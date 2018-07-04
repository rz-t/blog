from app.web import web
from app.model.resp import Resp
from app.utils import logger
from app.utils.exception import SecException
from flask import session, request


@web.app_errorhandler(SecException)
def sec_exception(e):
    """
    SecExcpetion
    """
    try:
        addr = request.remote_addr
        logger.error("{}: {}: {}".format(session.get('username'), addr, e))
    except Exception as ec:
        logger.error(ec)
    return Resp(Resp.ERROR, str(e)).to_json()


@web.app_errorhandler(Exception)
def exception(e):
    """
    所有异常
    """
    try:
        addr = request.remote_addr
        logger.error("{}: {}: {}".format(session.get('username'), addr, e))
    except Exception as ec:
        logger.error(ec)

    return Resp(Resp.ERROR, str(e)).to_json()