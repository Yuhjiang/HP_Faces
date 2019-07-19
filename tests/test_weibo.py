import unittest
from weibo.fetch_pictures import (fetch_json_response,
                                  fetch_pictures_info,
                                  fetch_pictures_info_url,
                                  fetch_pictures_info_advanced)
from weibo import MongoQueue, my_db


class TestFetchPictures(unittest.TestCase):
    # def setUp(self):
    #     queue = MongoQueue()
    #     queue.clear()

    def test_fetch_json_response(self):
        url = 'http://photo.weibo.com/photos/get_all?uid=2019518032&album_id=3555502164890927&count=30&page=2000&type=3&__rnd=1546678278092'
        res = fetch_json_response(url)

        self.assertTrue(res['result'] is True)

    def test_fetch_pictures_info(self):
        res = fetch_pictures_info(save=True)

        self.assertTrue(res is not [])

    def test_fetch_pictures_info_url(self):
        url = 'http://photo.weibo.com/photos/get_all?uid=2019518032&album_id=3555502164890927&count=30&page=2000&type=3&__rnd=1546678278092'
        res = fetch_pictures_info_url(url)

        self.assertTrue(res is not [])

    @unittest.skip
    def test_fetch_pictures_info_advanced(self):
        fetch_pictures_info_advanced(1, 10, save=True)

        images_db = my_db['images']
        image = images_db.find_one()
        self.assertTrue(image is not None)