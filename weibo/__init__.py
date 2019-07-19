from pymongo import MongoClient, errors
from config.config import Mongodb_uri
from datetime import datetime, timedelta


db_client = MongoClient(Mongodb_uri)
my_db = db_client['helloproject']


class MongoQueue(object):
    """
    多线程爬虫队列
    """
    OUTSTANDING = 1     # 初始态
    PROCESSING = 2      # 进行态
    COMPLETE = 3        # 完成态

    def __init__(self, db=Mongodb_uri, collection='mongo_queue', timeout=300):
        self.client = MongoClient(db)
        self.db = self.client['helloproject'][collection]
        self.timeout = timeout

    def __bool__(self):
        record = self.db.find_one(
            {'status': {'$ne': self.COMPLETE}}
        )
        return True if record else False

    def push(self, url):
        try:
            self.db.insert({'_id': url, 'status': self.OUTSTANDING})
            print(url, '进入队列')
        except errors.DuplicateKeyError as e:
            print(url, '已在队列中')

    def pop(self):
        record = self.db.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    def repush(self, url):
        record = self.db.find_and_modify(
            query={'_id': url},
            update={'$set': {'status': self.OUTSTANDING, 'timestamp': datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    def complete(self, url):
        self.db.update({'_id': url}, {'$set': {'status': self.COMPLETE}})

    def peek(self):
        record = self.db.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    def repair(self):
        """
        将所有超时的任务设为OUTSTANDING
        :return:
        """
        record = self.db.find_and_modify(
            query={
                'timestamp': {'$lt': datetime.now() - timedelta(seconds=self.timeout)},
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print('重置url状态', record['_id'])

    def clear(self):
        self.db.drop()