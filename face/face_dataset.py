"""
人脸库相关函数
1. 人脸注册
2. 人脸更新
"""
from face import client
import os
from utils.image import image_to_base64
import time


def face_detect(image, image_type):
    """
    人脸检测与人脸的质量
    :param image: 图片路径或者链接
    :param image_type: 本地图片 'BASE64'，URL图片 'URL'
    :return: {'error_code': 0, 'error_msg': 'SUCCESS',
    'log_id': 1368654435049675471, 'timestamp': 1563504967, 'cached': 0, 'result': {'face_num': 1, 'face_list':
    """
    if image_type == 'BASE64' and os.path.exists(image):
        image = image_to_base64(image)

    return client.detect(image, image_type)


def face_register(image_path):
    """
    将所有成员的人脸注册到百度云
    :param image_path: 人脸图片的存放路径
    """
    # ['angerme', 'beyooooonds', 'countrygirls', 'helloprokenshusei', 'helloprokenshuseihokkaido', 'juicejuice',
    # 'kobushifactory', 'morningmusume', 'tsubakifactory']
    group_dirs = os.listdir(image_path)

    for group_dir in group_dirs:
        members = os.listdir(os.path.join(image_path, group_dir))
        for m in members:
            # images\helloproject\angerme\akari_takeuchi.jpg
            path = os.path.join(image_path, group_dir, m)
            image = image_to_base64(path)
            res = client.addUser(image, 'BASE64', 'Hello_Project', m.split('.', 1)[0])
            time.sleep(0.5)     # QPS 2的限制，每秒请求不能超过2次


if __name__ == '__main__':
    m = 'yurina_kumai.jpg'
    path = os.path.join(r'E:\Program\Python\HP_Faces\images\helloproject\berryzkobo', m)
    image = image_to_base64(path)
    client.addUser(image, 'BASE64', 'Hello_Project', m.split('.', 1)[0])