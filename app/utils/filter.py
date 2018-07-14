from datetime import datetime
from app.model.node import Node as NodeModel

def format_time(_time):
    if isinstance(_time, datetime):
        return "{:04}-{:02}-{:02}".format(_time.year, _time.month, _time.day)
    return _time

def check_roles(roles, _roles=None):
    """
    检查角色是否满足（默认检查是否是admin）
    @param roles: 当前用户的角色(int)
    @param _roles: 要进行与运算的角色(int)
    """
    try:
        roles = int(roles)
    except Exception:
        return False
    try:
        _roles = int(_roles)
    except Exception:
        _roles = 1  # 1为管理员，默认检查是否是admin
    return roles & _roles != 0

def traverse_tree(tree, node_name):
    """
    遍历节点树
    前端使用
    """
    if isinstance(tree, (list, tuple, set)):
        if len(tree) > 0:
            resp = ['<ul>']
            for _ in tree:
                resp.append("{}".format(traverse_tree(_, node_name)))
            resp.append('</ul>')
            return ''.join(resp)
        return ""
    if isinstance(tree, NodeModel):
        return """
        <li>
            <a href='/{}/{}'>
                <span>{}</span>
            </a>
        </li>
        """.format(node_name, tree.id, tree.title)

    assert isinstance(tree, dict)
    t = list(tree.items())[0]
    return """
    <li class='has-sub'>
        <a href='/{}/{}'>
            <span>{}</span>
        </a>
        {}
    </li>
    """.format(node_name, t[0].id, t[0].title, traverse_tree(t[1], node_name))

def gen_intro(node, table):
    """
    根据node生成简介（可加缓存）
    @param node: 完整的NodeModel对象
    """
    assert isinstance(node, NodeModel)

    from app.lib.node import Node as NodeLib

    node_lib = NodeLib(table)

    try:
        if node.flag:   # 是文件夹则返回文件夹下面的文件
            node_list = node_lib.find_child_node(node.id)
            results = []
            for _ in node_list:
                results.append('<a href="/{}/{}" style="margin-right:13px;">{}</a>'.format(table, _.id, _.title))
            return ' '.join(results)
        else:   # 是文件则读取文件内容
            path = node_lib.final_path(node)
            with open(path) as f:
                result = f.read(256)
            return result
    except Exception:
        return ""