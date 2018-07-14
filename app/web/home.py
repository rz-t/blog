import os
from io import BytesIO
from app.web import web
from app.conf.misic import Misic as MisicConf
from app.lib.role import Role
from app.lib.vcode import gen_vcode
from app.lib.node import Node as NodeLib
from app.lib.user import login as user_login
from app.model.resp import Resp
from app.utils import logger
from app.utils.utils import templated, check_roles
from app.utils.exception import SecException
from app.forms.login import Login as LoginForm
from flask import request, session, Markup, make_response, flash, g


@web.before_app_request
def before():
    if not getattr(g, 'blog_tree', None):
        g.blog_tree = NodeLib('blog').find_node_tree(MisicConf.blog_tree_deep)
    if not getattr(g, 'note_tree', None):
        g.note_tree = NodeLib('note').find_node_tree(MisicConf.note_tree_deep)

@web.route("/favicon.ico")
def favicon():
    from app import app_path
    resp = make_response()
    resp.headers['Content-Type'] = 'image/git'
    with open("{}/favicon.ico".format(app_path), 'rb') as f:
        resp.set_data(f.read())
    return resp

@web.route("/")
@web.route("/home")
@templated("/home.html")
def home():
    """
    首页
    """
    note_lib = NodeLib('note')
    return {
        'node_list': note_lib.find_nodes()
    }

@web.route("/vcode")
def vcode():
    image, text = gen_vcode()
    buf = BytesIO()
    image.save(buf, 'jpeg')
    
    # 设置验证码返回
    resp = make_response(buf.getvalue())
    resp.headers['Content-Type'] = 'image/gif'

    # 验证码存入session中
    session['vcode'] = text
    return resp


@web.route("/login", methods=['POST'])
def login():
    addr = request.remote_addr
    form = LoginForm()

    if not form.validate():
        logger.info("{} ... {} ... {} login error...".format(addr, form.username.data, form.password.data))
        for error in form.errors.items():
            return Resp(Resp.ERROR, error).to_json()

    user = user_login(form.username.data, form.password.data)
    if user is None:
        logger.info("{} ... {} ... {} login error...".format(addr, form.username.data, form.password.data))
        return Resp(Resp.ERROR, '账号或密码错误').to_json()
    logger.info("{} ... {} login in...".format(addr, form.username.data))
    session['username'] = user.username
    session['roles'] = user.roles
    return Resp(Resp.SUCCESS).to_json()


@web.route("/admin")
@check_roles(Role.admin)
def admin():
    return "admin..."


@web.route("/normal")
@check_roles(Role.admin, Role.normal)
def normal():
    return "normal..."


@web.route("/about")
@templated("/about.html")
def about():
    from app import app_path
    """
    关于
    """
    with open(os.path.join(app_path, 'file', 'about.md')) as f:
        content = f.read()
    return {'content': content}

@web.route("/logout")
def logout():
    session.clear()
    return Resp(Resp.SUCCESS).to_json()