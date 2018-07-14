from app.utils.exception import SecException
from app.utils import database as db
from app.model.user import User as UserModel
from pymongo.database import Database


def login(username, password):
    """
    登陆成功返回查询出来的对象
    """
    try:
        user = getUserByName(username)
        if isinstance(user, UserModel) and user.username is not None:
            if user.check_password(password):
                return user
    except Exception as e:
        raise SecException(e)
    return None
    

def getUserByName(username):
    """
    根据username获取用户
    """
    assert isinstance(username, str)
    result = db.user.find_one({
        'username': username
    })
    return UserModel(result=result)