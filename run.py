#! /usr/bin/python3

from app import create_app
from app.utils import logger
from app.conf.flask import Misc

if __name__ == '__main__':
    logger.info("the app run in {}:{}".format(Misc.host, Misc.port))
    app = create_app()
    app.run(host=Misc.host, port=Misc.port)
