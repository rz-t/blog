from app import create_app
from app.lib.node import Node as NodeLib
from app.model.node import Node as NodeModel

def node_test():
    node_lib = NodeLib('note')

    # 开发
    note = NodeModel(title='开发')
    node_lib.create_node(note)

    _note = NodeModel(parent=note.id, title='书籍笔记')
    node_lib.create_node(_note)
    _note = NodeModel(parent=note.id, title='架构')
    node_lib.create_node(_note)
    _note = NodeModel(parent=note.id, title='安全工具')
    node_lib.create_node(_note)

    # 逆向
    note = NodeModel(title='逆向')
    node_lib.create_node(note)

    _note = NodeModel(parent=note.id, title='书籍笔记')
    node_lib.create_node(_note)
    _note = NodeModel(parent=note.id, title='工具')
    node_lib.create_node(_note)
    _note = NodeModel(parent=note.id, title='逆向分析')
    node_lib.create_node(_note)

    # 渗透
    note = NodeModel(title='渗透')
    node_lib.create_node(note)

    _note = NodeModel(parent=note.id, title='工具')
    node_lib.create_node(_note)

    # 系统
    note = NodeModel(title='系统')
    node_lib.create_node(note)
    
    _note = NodeModel(parent=note.id, title='windows')
    node_lib.create_node(_note)
    _note = NodeModel(parent=note.id, title='linux')
    node_lib.create_node(_note)

def print_tree(tree):
    if isinstance(tree, (list, tuple, set)):
        if len(tree) > 0:
            resp = ['<ul>']
            for _ in tree:
                resp.append("{}".format(print_tree(_)))
            resp.append('</ul>')
            return ''.join(resp)
        return ""
    if isinstance(tree, NodeModel):
        return """
        <li>
            <a href='#'>
                <span>{}</span>
            </a>
        </li>
        """.format(tree)

    assert isinstance(tree, dict)
    t = tree.popitem()
    return """
    <li class='has-sub'>
        <a href='#'>
            <span>{}</span>
        </a>
        {}
    </li>
    """.format(t[0], print_tree(t[1]))


if __name__ == '__main__':
    # node_test()
    node_lib = NodeLib('note')
    tree = node_lib.find_node_tree()

    print(print_tree(tree))
    pass