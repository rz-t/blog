import pymongo
from app.conf.db import DB as DBConf


class DB(object):
    def __init__(self, username=DBConf.username, password=DBConf.password, url=DBConf.url, db=DBConf.db):
        self.client = pymongo.MongoClient("mongodb://{}:{}@{}/{}".format(username, password, url, db))
        self.db = self.client[db]