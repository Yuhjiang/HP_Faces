"""
从微博爬取图片
"""
from weibo import my_db, MongoQueue
import requests
from config.config import headers, image_path
import json
from pymongo import errors
from utils.image import download_picture
import threading
import time

images_db = my_db['images']


def fetch_json_response(url):
    """
    首先获取json的图片信息
    :param url: 页面
    :return: json格式一页数据，30张图片
    """
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
        url = 'http://photo.weibo.com/photos/get_all?uid=2019518032&album_id=3555502164890927&count=30&page={}' \
              '&type=3&__rnd=1546678278092'.format(page)
        response = fetch_json_response(url)
        photo_list = response['data']['photo_list']

        for photo in photo_list:
            name = photo['pic_name']
            url = photo['pic_host'] + '/mw690/' + name
            timestamp = photo['timestamp']
            members = []

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

            if save is True:
                try:
                    images_db.insert_one(info)
                except errors.DuplicateKeyError:
                    pass

            members_from_page.append(info)

        return members_from_page


def fetch_pictures_info_url(url, save=False, download=False):
    """
    获取指定页面的图片信息
    :param url: 页面
    :param save: 是否保存到数据库
    :param download: 是否下载到本地
    :return:
    """
    members_from_page = []  # 需插入数据库的数据

    response = fetch_json_response(url)
    photo_list = response['data']['photo_list']

    for photo in photo_list:
        name = photo['pic_name']
        url = photo['pic_host'] + '/mw690/' + name
        timestamp = photo['timestamp']
        members = []

        info = {
            'name': name,
            'url': url,
            'timestamp': timestamp,
            'members': members,
            'downloaded': 0,
            'searched': 0,
        }

        if download is True:
            try:
                download_picture(url, image_path, name)
                info['downloaded'] = 1
            except:
                pass

        if save is True:
            try:
                images_db.insert_one(info)
            except errors.DuplicateKeyError:
                pass

        members_from_page.append(info)

    return members_from_page


def fetch_pictures_info_advanced(start=1, end=1, save=False, download=False, max_threads=10):
    """
    多线程获取指定页面的图片信息
    :param start: 开始页面
    :param end: 结束页面
    :param save: 是否保存到数据库
    :param download: 是否下载到本地
    :param max_threads: 最大线程数
    :return:
    """
    queue = MongoQueue()

    # for page in range(start, end):
    #     url = 'http://photo.weibo.com/photos/get_all?uid=2019518032&album_id=3555502164890927&count=30&page={}' \
    #           '&type=3&__rnd=1546678278092'.format(page)
    #     queue.push(url)

    def process_queue():
        while True:
            try:
                url = queue.pop()
                print(url)
            except KeyError:
                print('队列为空')
                break
            else:
                try:
                    fetch_pictures_info_url(url, save, download)
                    queue.complete(url)
                except:
                    queue.repush(url)

    threads = []
    while threads or queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)

        while len(threads) < max_threads or queue.peek():
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        time.sleep(1)


if __name__ == '__main__':
    # print(fetch_pictures_info(1, 1, save=True, download=True))
    # fetch_pictures_info_advanced(1, 7500, save=True, download=True)
    pass