import os
import random
import time
import shutil
from datetime import datetime
from bson.objectid import ObjectId
from app.__init__ import app_path
from app.utils import database as db
from app.model.node import Node as NodeModel
from app.utils.exception import SecException

class Node(object):
    
    def __init__(self, table):
        """
        @param table: 字符串，note or blog
        """
        assert Node.validate_table(table)

        self.table = table
    
    def create_node(self, node_model):
        assert isinstance(node_model, NodeModel)
        """
        创建节点
        """
        self.insert_node(node_model)  # 先插入数据库，成功后再创建物理节点

        try:
            # 查询出该节点的路径
            path = self.final_path(node_model)

            if not os.path.exists(path):
                if node_model.flag:         # flag为true，创建文件夹
                    os.makedirs(path)
                else:   # 否则创建文件
                    if not os.path.exists(os.path.dirname(path)):   # 判断文件所在目录是否存在，不存在则创建
                        os.makedirs(os.path.dirname(path))
                    with open(path, 'w'):   # 创建文件
                        pass
        except Exception as e:
            self.delete_node(node_model._id)
            raise e
        return node_model


    def final_path(self, node_model):
        """
        查询出物理路径，
        传入完整的对象
        若传入None，则返回根目录
        """
        if not node_model:
            return os.path.join(app_path, 'file', self.table)
        assert isinstance(node_model, NodeModel)

        path = [node_model.title]
        node = self.find_node(node_model.parent)  # 查询父节点
        while node:
            path.append(node.title)
            node = self.find_node(node.parent)
        path = path[::-1]
        path = os.path.join(app_path, 'file', self.table, *path) # 最终路径
        return path

    def node_content(self, node_model):
        """
        查询出node_model对应的内容
        传入完整的对象
        若传入文件夹或对应的文件不存在则抛异常
        """
        path = self.final_path(node_model)
        assert os.path.isfile(path)

        with open(path) as f:
            content = f.read()
        return content

    def drop_node(self, _id):
        """
        删除一个节点,
        数据库删除
        物理文件重命名
        """
        node = self.find_node(_id)
        path = self.final_path(node)

        if os.path.exists(path):    # 如果存在则重命名
            node_dir = os.path.dirname(path)
            shutil.move(path, '{}/del_{}_{}_{}' # 路径/del_时间_随机数_原文件名
                .format(node_dir, time.ctime().replace(' ', '-'), str(random.randrange(100000)), node.title))
        self.delete_node(_id)     # 数据库删除

    def find_nodes(self, num=3, flag=False):
        """
        按更新日期排序查找节点
        @param num: 要查找节点的数量
        @param flag: False则按时间倒序查，True则按时间正序查
        """
        assert isinstance(num, int)
        assert isinstance(flag, bool)
        db_node = db[self.table]

        node_list = db_node.find({
            'flag': False
        }).limit(num).sort([('update_time',-1)])

        return [NodeModel(result=node) for node in node_list]

    def find_node(self, _id):
        """
        查询出_id对应的节点信息
        _id为None或查询不到返回None
        """
        if _id is None:
            return None
        db_node = db[self.table]

        result = db_node.find_one({
            '_id': ObjectId(_id)
        })

        return NodeModel(result=result) if result is not None else None


    def find_parent_node(self, node_model):
        """
        查询node_model的父节点列表信息
        @return: [父节点， 父父节点， 父父父节点, ...]
        """
        if not isinstance(node_model, NodeModel) or not node_model.parent:
            return []
        node_list = []
        node = self.find_node(node_model.parent)
        while node:
            node_list.append(node)
            node = self.find_node(node.parent)
        return node_list[::-1]


    def find_child_node(self, _id=None, limit=0, skip=0):
        """
        查询出父节点为_id的节点信息
        @param limit: 查询数量
        按更新日期降序排列
        先文件夹后文件
        """
        assert isinstance(limit, int)
        assert isinstance(skip, int)

        db_node = db[self.table]
        try:
            node_list = db_node.find({
                'parent': _id
            }).skip(skip).limit(limit).sort([('flag', -1), ('update_time',-1)])
            return [NodeModel(result=node) for node in node_list]
        except Exception as e:
            raise SecException(e)


    def find_node_tree(self, depth=None):
        """
        节点树
        @param depth: 深度，0则只有一级目录，依次递增

        文件夹用 {NodeModel: []} 表示
        文件用 NodeModel表示
        """
        tree = []
        for _node in self.find_child_node():
            tree.append(self.node_tree(_node, depth))
        return tree
    
    def node_tree(self, node, depth=None):
        """
        递归查找
        @param depth: 深度
        """
        if isinstance(depth, int):   # 深度
            if not hasattr(self, 'depth'):
                self.depth = 0
            self.depth += 1
            if self.depth > depth:
                return node

        assert isinstance(node, NodeModel)
        result = None

        if not node.flag:   # 说明是文件，直接返回即可
            result = node
        else:
            # 说明是文件夹
            child_nodes = self.find_child_node(node.id)
            result = {
                node:[
                    self.node_tree(child) for child in child_nodes
                ]
            }
        
        if isinstance(depth, int):  # 深度
            assert hasattr(self, 'depth')
            self.depth -= 1
        
        return result


    def edit_content(self, node_model, content):
        """
        更新node文件里的内容
        """
        assert isinstance(node_model, NodeModel)
        assert isinstance(content, str)

        path = self.final_path(node_model)
        if not os.path.isfile(path):
            raise SecException('文件不存在！{}'.format(path))
        
        with open(path, 'w') as f:
            f.write(content)
            
    def edit_title(self, node_model, title):
        """
        更新title
        """
        assert isinstance(node_model, NodeModel)
        assert isinstance(title, str)
        title = title.strip()
        assert len(title) > 0

        db_node = db[self.table]
        path = self.final_path(node_model)
        if not os.path.exists(path):
            raise SecException('文件(夹)不存在！{}'.format(path))

        try:
            # 修改数据库
            db_node.update({
                '_id': ObjectId(node_model.id)
            }, {
                '$set':{
                    'title': title
                }
            })

            # 修改物理路径
            sep = os.path.sep   # 获取操作系统的路径分割符
            _ = path.split(sep)
            l = len(_)

            for i in range(l, 0, -1):   # 修改这个文件(夹)的名称
                i -= 1
                if len(_[i].strip()) == 0:
                    continue
                _[i] = title
                break
            shutil.move(path, sep.join(_))  # 移动物理路径
        except Exception as e:  # 出错后回滚
            db_node.update_one({
                'id': ObjectId(node_model.id)
            }, {
                '$set':{
                    'title': node_model.title
                }
            })
            raise SecException(e)
        

    def delete_node(self, _id):
        """
        删除数据库中的节点（改为逻辑删除）
        @param _id: _id
        """
        assert _id is not None

        db_node = db[self.table]
        result = db_node.delete_one({
            '_id': ObjectId(_id)
        })
        
        return result.deleted_count


    def insert_node(self, node_model):
        """
        将节点插入数据库
        @param node_model: NodeModel
        """
        assert isinstance(node_model, NodeModel)

        db_node = db[self.table]
        try:
            curr_time = datetime.utcnow()
            _id = db_node.insert_one({
                'parent': node_model.parent,
                'title': node_model.title,
                'flag': node_model.flag,
                'create_time': curr_time,
                'update_time': curr_time
            }).inserted_id

            if _id is None:
                raise SecException('{}插入失败'.format(self.table))
        except Exception as e:
            raise SecException(e)

        node_model.id = _id # 将生成的id返回至原对象中
        return node_model

    def move_node(self, _id, target_parent_id):
        """
        移动_id节点到target_parent_id目录下
        @param _id: 可以是文件/文件夹
        @param target_parent_id: 必须是文件夹，且不能是_id文件夹的子文件夹
        """
        node_model = self.find_node(_id)
        parent_model = None
        if target_parent_id:    #如果是None，则移到根目录
            parent_model = self.find_node(target_parent_id) # 父节点
            if not parent_model.flag:
                raise SecException('目标必须是文件夹')

        src_file = self.final_path(node_model)  # 源路径
        dst_path = self.final_path(parent_model)    # 目的文件夹

        if dst_path.startswith(src_file):
            raise SecException('不可以移动至子文件夹中')
        
        if not os.path.exists(src_file):
            raise SecException('源文件（夹）不存在')
        if not os.path.isdir(dst_path):
            raise SecException('目标文件夹不存在')
        
        db_node = db[self.table]
        try:
            # 先修改数据库
            db_node.update_one({
                '_id': ObjectId(node_model.id)
            },{
                '$set':{
                    'parent': target_parent_id
                }
            })

            # 修改物理文件
            shutil.move(src_file, dst_path)
        except Exception as e:
            # 回滚
            db_node.update_one({
                '_id': ObjectId(node_model.id)
            },{
                '$set':{
                    'parent': node_model.parent
                }
            })
            raise SecException(e)

    @staticmethod
    def validate_table(table):
        """
        校验table是否有效
        """
        return 'note' == table or 'blog' == table
