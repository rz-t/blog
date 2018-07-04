import re
import json
from app.model.resp import Resp
from app.web import web
from app.forms.node import Node as NodeForm
from app.lib.node import Node as NodeLib
from app.model.node import Node as NodeModel
from app.lib.role import Role
from app.utils.utils import templated, check_roles, check_roles_func
from app.utils.exception import SecException
from flask import request, session, render_template, redirect, url_for, g

@web.route("/note/")
@web.route("/note/<_id>")
def note(_id=None):
    """
    如果是文件，则直接返回markdown数据
    如果markdown的数据为空，且当前用户为管理员，则直接进入编辑状态
    如果文件夹，则返回包含子节点列表
    """
    node_lib = NodeLib('note')
    node = node_lib.find_node(_id)

    if not isinstance(node, NodeModel):
        _id = None

    parent_list = node_lib.find_parent_node(node)

    if _id is None or node.flag:   # 文件夹，默认主目录
        node_list = node_lib.find_child_node(_id)
        return render_template("note.html", node_list=node_list, parent_list=parent_list, node_model=node)
    else:           # 文件
        content = node_lib.node_content(node)
        if check_roles_func(Role.admin) and len(str(content).strip()) == 0: # 如果是管理员且该文件无内容，则直接重定向至编辑器
            return redirect(url_for('web.note_editor', _id=_id))
        return render_template("note-show.html", content=content, parent_list=parent_list, node_model=node)

@web.route("/note/delete/<_id>", methods=['POST'])
@check_roles(Role.admin)
def note_delete(_id):
    """
    删除note节点
    """
    node_lib = NodeLib('note')
    if not re.match(r'^[\d\w]{24,26}$', str(_id)):
        raise SecException('id有误')

    node_lib.drop_node(_id)
    return Resp(Resp.SUCCESS).to_json()

@web.route("/note/add/", methods=['POST'])
@web.route("/note/add/<_id>", methods=['POST'])
@check_roles(Role.admin)
def note_add(_id=None):
    """
    在_id的节点下添加文件（夹）
    """
    node_lib = NodeLib('note')

    form = request.form

    if _id and not re.match(r'^[\d\w]{24,26}$', str(_id)):
        raise SecException('id有误')
    if not re.match(r'^[\d\w-]+$', str(form.get('title'))):
        raise SecException('title有误！')
    node_model = NodeModel(parent=_id, title=form.get('title'), flag=bool(int(form.get('flag'))))

    node_lib.create_node(node_model)
    return Resp(Resp.SUCCESS).to_json()


@web.route("/note/edit/content/<_id>", methods=['POST'])
@check_roles(Role.admin)
def note_edit_content(_id):
    """
    修改note内容
    """
    node_lib = NodeLib('note')
    node = node_lib.find_node(_id)

    if not isinstance(node, NodeModel):
        raise SecException('不存在的note: {}'.format(_id))
    if 'content' not in request.form:
        raise SecException('缺少参数！')
    
    node_lib.edit_content(node, request.form['content'])

    return Resp(Resp.SUCCESS, '修改成功！').to_json()

@web.route("/note/edit/title/<_id>", methods=['POST'])
@web.route("/note/edit/title/", methods=['POST'])
@check_roles(Role.admin)
def note_edit_title(_id):
    """
    修改note文件（夹）的标题
    """
    node_lib = NodeLib('note')
    node_model = node_lib.find_node(_id)
    
    form = request.form
    if 'new_title' not in form:
        raise SecException('缺少参数！')

    if not re.match(r'^[\d\w]{24,26}$', str(_id)) or not re.match(r'^[\d\w-]+$', str(form['new_title'])):
        raise SecException('参数有误！')

    node_lib.edit_title(node_model, form['new_title'])

    return Resp(Resp.SUCCESS, request.form['new_title']).to_json()

@web.route("/note/edit/<_id>")
@templated("note-editor.html")
@check_roles(Role.admin)
def note_editor(_id):
    """
    note编辑器
    """
    node_lib = NodeLib('note')
    node = node_lib.find_node(_id)

    if not isinstance(node, NodeModel):
        raise SecException('不存在的note: {}'.format(_id))
    return {
        'node_model': node,
        'content': node_lib.node_content(node)
    }

@web.route("/note/cut/<_id>", methods=['POST'])
@check_roles(Role.admin)
def note_cut(_id):
    """
    剪切
    """
    if not re.match(r'^[\d\w]{24,26}$', str(_id)):
        raise SecException('_id有误！{}'.format(_id))
    session['note_cut_id'] = _id    # 设置标志
    return Resp(Resp.SUCCESS).to_json()

@web.route("/note/paste/", methods=['POST'])
@web.route("/note/paste/<_id>", methods=['POST'])
@check_roles(Role.admin)
def note_paste(_id=None):
    """
    粘贴
    要求session中存在 note_cut_id
    """
    if 'note_cut_id' not in session:
        raise SecException('session中不存在源id')
    
    if _id and not re.match(r'^[\d\w]{24,26}$', str(_id)):
        raise SecException('_id有误！{}'.format(_id))
    
    node_lib = NodeLib('note')
    node_lib.move_node(session['note_cut_id'], _id)

    del session['note_cut_id']
    return Resp(Resp.SUCCESS).to_json()

@web.route("/note/cancel/cut", methods=['POST'])
@check_roles(Role.admin)
def note_cancel_cut():
    """
    取消剪切
    """
    if 'note_cut_id' in session:
        del session['note_cut_id']
    return Resp(Resp.SUCCESS).to_json()