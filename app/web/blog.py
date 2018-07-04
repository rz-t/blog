from app.web import web
from app.lib.node import Node as NodeLib
from app.model.node import Node as NodeModel
from app.utils.utils import templated
from app.utils.exception import SecException
from flask import request, session, render_template

@web.route("/blog/")
@web.route("/blog/<_id>")
def blog(_id=None):
    """
    如果是文件，则直接返回markdown数据
    如果文件夹，则返回包含子节点列表
    """
    node_lib = NodeLib('blog')
    node = node_lib.find_node(_id)

    if not isinstance(node, NodeModel):
        _id = None

    if _id is None or node.flag:   # 文件夹，默认主目录
        node_list = node_lib.find_child_node(_id)
        return render_template("blog.html", node_list=node_list)
    else:           # 文件
        pass