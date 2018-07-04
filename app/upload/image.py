import json
import os
from app.utils import logger
from app.conf.misic import Misic
from app.upload import upload
from app.lib.upload import file_save
from app.lib.role import Role
from app.utils.utils import templated, check_roles
from app.utils.exception import SecException
from flask import request, session, render_template, send_from_directory, url_for


@upload.route("/upload/img/", methods=['POST'])
@check_roles(Role.admin)
def upload_img():
    logger.info("{} upload img {}".format(session.get('username'), request.files))
    from app import app_path

    if 'editormd-image-file' not in request.files:
        raise SecException('上传失败！')
    img = request.files['editormd-image-file']
    
    if not img.filename:
        raise SecException('没有选择文件')
    
    
    name = file_save(img, Misic.img_suffix, os.path.join(app_path, 'file/', 'images/'))

    return json.dumps({
        'success': 1,   # 0失败，1成功
        'message': '上传成功！',    # 失败时回显
        'url': url_for('upload.download_img', name=name)   # 下载的地址
    })

@upload.route("/images/<name>")
@check_roles(Role.admin)
def download_img(name):
    logger.info("{} download img {}".format(session.get('username'), name))
    from app import app_path
    return send_from_directory(os.path.join(app_path, 'file', 'images'), name, as_attachment=True)
    
