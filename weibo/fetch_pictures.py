"""
从微博爬取图片
"""
from weibo import my_db
import requests
from config.config import headers, image_path
import json
from utils.image import download_picture


images_db = my_db['images']


def fetch_json_response(page):
    """
    首先获取json的图片信息
    :param page: 页码
    :return: json格式一页数据，30张图片
    """
    url = 'http://photo.weibo.com/photos/get_all?uid=2019518032&album_id=3555502164890927&count=30&page={}' \
          '&type=3&__rnd=1546678278092'.format(page)
    res = requests.get(url, headers=headers).text
    res = json.loads(res)

    if not res['result']:
        raise Exception('Failed to download the data', url)
    else:
        return res


def fetch_pictures_info(start=1, end=1, save=False, download=False):
    """
    获取指定页面的图片信息
    :param start: 开始页面
    :param end: 结束页面
    :param save: 是否保存到数据库
    :param download: 是否下载到本地
    :return:
    """
    members_from_page = []  # 需插入数据库的数据

    for page in range(start, end + 1):
        response = fetch_json_response(page)
        photo_list = response['data']['photo_list']

        for photo in photo_list:
            name = photo['pic_name']
            url = photo['pic_host'] + '/mw690/' + name
            timestamp = photo['timestamp']
            members = []

            # if images_db.find_one({'name': name}):
            #     continue
            info = {
                'name': name,
                'url': url,
                'timestamp': timestamp,
                'members': members,
                'downloaded': 0,
                'searched': 0,
            }

            if download is True:
                download_picture(url, image_path, name)
                info['downloaded'] = 1

            members_from_page.append(info)

        if save is True:
            images_db.insert_many(members_from_page)

        return members_from_page


if __name__ == '__main__':
    images_db.drop()
    images_db = my_db['images']
    print(fetch_pictures_info(1, 1, save=True, download=True))