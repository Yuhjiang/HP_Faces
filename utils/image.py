import requests
import os


def valid_image(image):
    """
    判断是否成功下载了image
    :param image: request.get()的对象
    """
    return image.history == []


def download_picture(url, path, name, **kwargs):
    """
    下载图片
    :param url: 图片链接
    :param path: 保存位置
    :param name: 图片名
    :param kwargs: headers信息
    """
    image = requests.get(url, **kwargs)
    if not valid_image(image):
        raise Exception('Failed to download the picture', url)

    if not os.path.exists(path):
        raise Exception('Invalid path')

    image_path = os.path.join(path, name)
    with open(image_path, 'ab') as f:
        f.write(image.content)
