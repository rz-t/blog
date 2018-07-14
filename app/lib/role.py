from enum import Enum, unique
from app.utils.exception import SecException

class Role(Enum):
    admin   = 0b00000001        # 管理员
    normal  = 0b00000010        # 普通用户


def gen_value(*roles):
    """
    根据role列表生成value
    @param: roles 可以是字符串列表也可以是Role列表
    """
    value = 0
    for role in roles:
        if isinstance(role, str):
            role = Role[role]
        assert isinstance(role, Role)
        
        value |= role.value
    return value


def gen_roles(value):
    """
    根据value总值生成name列表（Role类型）
    @param: value 接受整形
    """
    assert isinstance(value, int)
    names = []
    for role in Role.__iter__():
        if value & role.value != 0:
            names.append(role)
    return names


if __name__ == '__main__':
    value = gen_value('admin', Role.normal)
    print("value", value)
    roles = gen_roles(value)
    print(roles)

    value = gen_value('normal', Role.normal)
    print("value", value)
    roles = gen_roles(value)
    print(roles)
