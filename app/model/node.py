from datetime import datetime

class Node(object):
    """
    节点模型类
    note与blog都用这个类
    """
    def __init__(self, _id=None, parent=None, title=None, flag=True,
        create_time=None, update_time=None, result=None):
        """
        @param _id: id
        @param parent: 父目录id
        @param title: 标题
        @param flag: 是否是文件夹   默认是文件夹
        @param create_time: 创建时间
        @param update_time: 更新时间
        @result: 接收字典，用于数据库查询时生成实体对象
        """
        if isinstance(result, dict):
            self.__dict__ = result
        else:
            self.id = _id
            self.parent = parent
            self.title = title
            self.flag = flag
            self.create_time = create_time if isinstance(create_time, datetime) else None
            self.update_time = update_time if isinstance(update_time, datetime) else None
    
    @property
    def id(self):
        return str(self._id)
    
    @id.setter
    def id(self, value):
        self._id = str(value)

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return self.__dict__.__str__()