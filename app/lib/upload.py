import os
import random
import time
from werkzeug.datastructures import FileStorage
from app.utils.exception import SecException

def file_save(_file, _suffix, _path):
    """
    保存文件
    @param _file: FileStorage
    @param _suffix: 文件后缀（可以是列表，也可以是字符串）
    @param _path: 要存储的路径
    """
    assert isinstance(_file, FileStorage)
    assert isinstance(_suffix, (str, list, set, tuple))
    assert isinstance(_path, str)

    _path = os.path.dirname(_path)
    filename = _file.filename

    _ = filename.rsplit('.', 1)
    if len(_) != 2:
        raise SecException('文件名有误！{}'.format(filename))
    suf = _[1]

    if suf not in _suffix:
        raise SecException('文件后缀有误！{}'.format(filename))
    
    name = '{}_{}'.format(time.ctime().replace(' ', '-'), random.randrange(100000, 1000000))

    try:
        _file.save(os.path.join(_path, '{}.{}'.format(name.rstrip('/'), suf)))
    except Exception as e:
        raise SecException(e)
    finally:
        _file.close()
    
    return '{}.{}'.format(name, suf)