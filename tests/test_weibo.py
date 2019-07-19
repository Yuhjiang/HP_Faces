import unittest
from weibo.fetch_pictures import (fetch_json_response,
                                  fetch_pictures_info)


class TestFetchPictures(unittest.TestCase):
    def test_fetch_json_response(self):
        res = fetch_json_response(1)

        self.assertTrue(res['result'] is True)

    def test_fetch_pictures_info(self):
        res = fetch_pictures_info(save=True)

        self.assertTrue(res is not [])