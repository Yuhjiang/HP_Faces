import unittest
import pymongo
from config.config import Mongodb_uri


class TestFaceSearch(unittest.TestCase):
    def setUp(self):
        db_client = pymongo.MongoClient(Mongodb_uri)
        my_db = db_client['helloproject']
        images_db = my_db['images']

        images_db.update_one({'name': '785f6650gy1g54e5db3g7j20u00u0n95.jpg'},
                             {'$set': {'members': []}})

    # def test_face_multi_search(self):
    #
