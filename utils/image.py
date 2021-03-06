import requests
import os
import base64


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
        os.mkdir(path)

    image_path = os.path.join(path, name)
    with open(image_path, 'ab') as f:
        f.write(image.content)


def image_to_base64(image_path):
    """
    图片的base64值
    :param image_path: 图片位置
    :return: base64值
    """
    with open(image_path, 'rb') as image:
        image_base64 = base64.b64encode(image.read())

    return image_base64.decode('utf-8')


if __name__ == '__main__':
    print(image_to_base64('../images/morningmusume/mizuki_fukumura.jpg'))