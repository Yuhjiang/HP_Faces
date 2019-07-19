import unittest
import pymongo
from config.config import Mongodb_uri
from face.face_search import (face_to_databases,
                              face_multi_search)

db_client = pymongo.MongoClient(Mongodb_uri)
my_db = db_client['helloproject']
images_db = my_db['images']


class TestFaceSearch(unittest.TestCase):
    def setUp(self):

        images_db.update_one({'name': '785f6650gy1g54e5db3g7j20u00u0n95.jpg'},
                             {'$set': {'members': []}})

    def test_face_multi_search(self):
        image = images_db.find_one({'name': '785f6650gy1g54e5db3g7j20u00u0n95.jpg'})
        res = face_multi_search(image, 'BASE64')

        self.assertTrue(res['error_msg'] == 'SUCCESS')

    def test_face_to_databases(self):
        image = images_db.find_one({'name': '785f6650gy1g54e5db3g7j20u00u0n95.jpg'})
        res = face_multi_search(image, 'BASE64')
        face_to_databases(image, res)

        image = images_db.find_one({'name': '785f6650gy1g54e5db3g7j20u00u0n95.jpg'})

        self.assertTrue(image['members'][0]['name_en'] == 'ayaka_wada')