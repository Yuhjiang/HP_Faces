"""
测试face模块
"""

import unittest
from face import client
import time
from face.face_dataset import (face_detect,
                               face_register)


class TestFaceDataset(unittest.TestCase):
    # def setUp(self):
    #     members = client.getGroupUsers('Hello_Project')
    #     if 'mizuki_fukumura' in members['result']['user_id_list']:
    #         client.deleteUser('Hello_Project', 'mizuki_fukumura')
    #
    # def tearDown(self):
    #     members = client.getGroupUsers('Hello_Project')
    #     if 'mizuki_fukumura' in members['result']['user_id_list']:
    #         client.deleteUser('Hello_Project', 'mizuki_fukumura')
    @unittest.skip
    def test_face_detect(self):
        res = face_detect('../images/helloproject/morningmusume/mizuki_fukumura.jpg', 'BASE64')
        time.sleep(0.5)
        self.assertTrue(res['error_code'] == 0 and res['error_msg'] == 'SUCCESS')

    @unittest.skip
    def test_face_register(self):
        face_register('../images/helloproject')
        res = client.getGroupUsers('Hello_Project')

        self.assertTrue('mizuki_fukumura' in res['result']['user_id_list'])