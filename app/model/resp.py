import json

class Resp(object):
    SUCCESS = "success"
    ERROR = "error"
    
    """
    返回json数据统一格式
    """
    def __init__(self, flag, data=None):
        assert flag in [Resp.SUCCESS, Resp.ERROR]
        self.flag = flag
        self.data = data
    
    def to_json(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.__str__()   