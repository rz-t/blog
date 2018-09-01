from app.web import web
from app.conf.wooyun import Wooyun as WooyunConf
from app.lib.wooyun import query_keyword
from app.utils.utils import templated
from app.utils.exception import SecException
from flask import request, session, render_template

limit = 15  # 每页的数量

@web.route("/wy", methods=['POST', 'GET'])
def wooyun():
    """
    乌云drop
    """
    if request.method == 'GET':
        return render_template("wooyun.html")
    print(request.form)
    start = request.form.get('start')
    try:
        start = int(start)
        if start < 1 or start > 10000:  # 最多展示1W页
            raise SecException()
    except Exception:
        start = 1   # 默认第一页
    drop_list, count, max_page = query_keyword(request.form['keyword'], start)

    return render_template("wooyun-list.html", keyword=request.form['keyword'],
        drop_list=drop_list, start=start, max_page=max_page, count=count, uri=WooyunConf.uri)
