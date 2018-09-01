class Config(object):
    pass

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True

class Misc(object):
    host = '0.0.0.0'
    port = '7788'
