class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True

class Misc(object):
    host = '127.0.0.1'
    port = '7788'
