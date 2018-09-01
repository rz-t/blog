import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.web import web
from app.upload import upload
from app.utils.filter import traverse_tree, format_time, gen_intro, check_roles
from app.conf.flask import DevConfig, ProdConfig
from flaskext.markdown import Markdown

app_path = os.path.dirname(os.path.realpath(__file__))

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_object(ProdConfig)

    app.register_blueprint(web)
    app.register_blueprint(upload)

    csrf.init_app(app)

    csrf.exempt(upload)

    Markdown(app)

    app.add_template_filter(traverse_tree)  # 过滤器
    app.add_template_filter(format_time)  # 过滤器
    app.add_template_filter(gen_intro)  # 过滤器
    app.add_template_filter(check_roles) # 过滤器 角色校验

    return app
