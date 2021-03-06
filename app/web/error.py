from app.web import web
from app.model.resp import Resp
from app.utils import logger
from app.utils.exception import SecException
from flask import session, request, make_response


@web.app_errorhandler(SecException)
def sec_exception(e):
    """
    SecExcpetion
    """
    try:
        addr = request.remote_addr
        logger.error("{}: {}:".format(session.get('username'), addr), exc_info=1)
    except Exception as ec:
        logger.exception(ec)
    resp = make_response(Resp(Resp.ERROR, str(e)).to_json(), 200)
    resp.headers['Content-Type'] = "application/json"
    return resp


@web.app_errorhandler(Exception)
def exception(e):
    """
    所有异常
    """
    try:
        addr = request.remote_addr
        logger.error("{}: {}:".format(session.get('username'), addr), exc_info=1)
    except Exception as ec:
        logger.exception(ec)

    resp = make_response(Resp(Resp.ERROR, str(e)).to_json(), 200)
    resp.headers['Content-Type'] = "application/json"
    return resp
