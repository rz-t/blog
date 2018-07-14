import re
import math
from app.utils.exception import SecException
from app.utils import database as db
from pymongo.database import Database

def deal_keyword(keyword):
    """
    处理keyword
    @param: keyword title:xxx author:xxx 默认两个都查询
            查询原则： (title1 or title2 or title3) and (author1 or author2 or author3) 
            and normal1 and normal2 and normal3
    @return: 处理后的数据：titles，authors，normals
    """
    keyword = str(keyword).strip()

    titles = re.findall(r'title\s*:\s*\S+', keyword)
    for title in titles:
        keyword = keyword.replace(title, '')
    
    authors = re.findall(r'author\s*:\s*\S+', keyword)
    for author in authors:
        keyword = keyword.replace(author, '')
    
    normals = re.split(r'\s+', keyword)
    _normal = [_ for _ in normals if _ != '']

    _title = []
    for title in titles:
        title = re.sub(r'title\s*:\s*', '', title)
        _title.append(title)
    
    _author = []
    for author in authors:
        author = re.sub(r'author\s*:\s*', '', author)
        _author.append(author)
    return _normal, _title, _author


def deal_array(arr):
    """
    处理数组列表，使其变为模糊查询
    """
    assert isinstance(arr, (list, set, tuple))
    _arr = []
    for s in arr:
        _arr.append(re.compile('^.*{}.*$'.format(s), re.RegexFlag.I))   # 模糊查询
    return _arr


def query_keyword(keyword, start, limit = 15):
    """
    处理keyword
    @param: keyword title:xxx author:xxx 默认两个都查询
            查询原则： (title1 or title2 or title3) and (author1 or author2 or author3) 
            and normal1 and normal2 and normal3
    @param: start 开始页数
    @return: 结果列表，总数，总页数
    """
    assert isinstance(db, Database)
    assert isinstance(start, int)

    sec = db.sec

    normals, titles, authors = deal_keyword(keyword)
    titles = deal_array(titles)
    authors = deal_array(authors)
    normals = deal_array(normals)

    _and = []
    if len(authors) != 0:
        _and.append({
            'author':{
                '$in': authors
            }
        })
    if len(titles) != 0:
        _and.append({
            'title':{
                '$in': titles
            }
        })
    if len(normals) != 0:
        _and.append({
            '$or':[
                {
                    'author': {
                        '$in': normals
                    }
                },
                {
                    'title': {
                        '$in': normals
                    }
                }
            ]
        })
    
    target = sec.find({
        '$and': _and
    } if len(_and) != 0 else {})

    count = target.count()
    return target.skip((start - 1) * limit).limit(limit), count, math.ceil(count / limit)


""" 查询示意
find(
    {
        '$and':[
            {
                'author': {
                    '$in': ['tom', 'john']
                }
            },
            {
                'title': {
                    '$in': ['web', '逆向']
                }
            },
            {
                '$or': [
                    {
                        'author': {
                            '$in': ['aab', 'bbc', 'dde']
                        }
                    },
                    {
                        'title': {
                            '$in': ['aab', 'bbc', 'dde']
                        }
                    }
                ]
            }
        ]
    }
)
"""