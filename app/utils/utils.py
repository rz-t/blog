import functools
from app.lib.role import Role, gen_roles, gen_value
from app.utils.exception import SecException
from flask import request, render_template, session, redirect, url_for


def check_login(func):
    """
    登陆检查
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('web.home'))
        return func(*args, **kwargs)
    return wrapper


def check_roles(*roles):
    """
    权限校验
    @param roles: 接收字符串或Role类型
    """
    def check(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if check_roles_func(*roles):
                return func(*args, **kwargs)
            return redirect(url_for('web.home'))
        return wrapper
    return check

def check_roles_func(*roles):
    """
    权限校验，返回 True or False
    """
    if 'roles' not in session:
        return False
    curr_role = int(session['roles'])

    value = gen_value(*roles)
    if curr_role & value == 0:
        return False
    return True

def compose_route(route, *decs):
    """
    联合包装器
    :param route: app.route、blueprint.route
    :param decs:
    :return:
    """
    def func_route(rule, **options):
        def wrapper(func):
            for dec in reversed(decs):
                func = dec(func)
            return route(rule, **options)(func)
        return wrapper
    return func_route


def templated(template=None):
    """
    模板装饰器
    :param template:
    :return:
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator