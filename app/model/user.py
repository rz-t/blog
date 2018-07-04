from werkzeug.security import generate_password_hash, check_password_hash

class User(object):
    """
    用户类
    """
    def __init__(self, username=None, password=None, roles=None, result=None):
        """
        result，接受字典类型，一般为数据库中查询的值
        """
        if isinstance(result, dict):
            self.username = result['username']
            self._password = result['password']
            self.roles = result['roles']
        else:
            self.username = username
            self.password = password
            self.roles = roles
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            self._password = None
        else:
            self._password = generate_password_hash(value)
    
    def check_password(self, value):
        assert isinstance(value, str)
        return check_password_hash(self.password, value)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{}, {}, {}".format(self.username, self.password, self.roles)