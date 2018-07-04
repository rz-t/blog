import logging
from app.utils.db import DB

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: '
                                                '%(message)s')

# 日志
logger = logging.getLogger(__name__)


# 数据库
_db = DB()
client = _db.client
database = _db.db