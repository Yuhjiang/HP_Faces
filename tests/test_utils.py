"""
测试utils模块
"""

import unittest
import os
from utils.image import (download_picture,
                         image_to_base64)


class TestUtilsImage(unittest.TestCase):
    def tearDown(self):
        if os.path.exists('../images/test.jpg'):
            os.remove('../images/test.jpg')

    @unittest.skip
    def test_download_picture(self):
        url = 'http://cdn.helloproject.com/img/artist/m/90b7c2d8312bf4323fe7b835ac4561ef2d7ee9b6.jpg'
        path = '../images'
        name = 'test.jpg'

        download_picture(url, path, name)

    def test_image_to_base64(self):
        image_base64 = image_to_base64('../images/helloproject/morningmusume/mizuki_fukumura.jpg')

        self.assertTrue(image_base64 is not None)
