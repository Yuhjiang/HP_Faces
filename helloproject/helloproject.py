"""
处理www.helloproject.com页面的模块
1. 收集成员信息
"""


import requests
import bs4
import pymongo
import os
from config.config import Mongodb_uri
from utils.image import download_picture


def fetch_artist_page(url='http://www.helloproject.com/artist/') -> list:
    """
    获取官网各个组合的网页
    :param url: 默认为 http://www.helloproject.com/artist/
    :return: [morning_musume._page, angerme_page,...] 各个组合的网页
    """
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    # 获取所有组合的信息
    # <a href="/morningmusume/"><img alt="モーニング娘。'19"
    # src="http://cdn.helloproject.com/img/artist/m/3296cb5f462ebf509f27f921061d22a9fe4a53f8.jpg"/></a>
    groups = soup.select('.artist_listbox a')

    # 格式化信息
    group_list = []
    for group in groups:
        group_url = 'http://www.helloproject.com' + group.get('href') + 'profile'
        # http://www.helloproject.com/morningmusume/profile/
        name_en = group.get('href')[1:-1]                                   # morningmusume
        name_jp = group.select('img')[0].get('alt')                         # "モーニング娘。'19"

        group_list.append({'url': group_url,
                           'name_en': name_en,
                           'name_jp': name_jp})

    return group_list


def group_to_database(groups):
    """
    将数据添加到mongodb中
    :param groups: [morning_musume._page, angerme_page,...]
    """
    client = pymongo.MongoClient(Mongodb_uri)
    my_db = client['helloproject']
    group_db = my_db['groups']
    group_db.insert_many(groups)


def members_from_profile(url, download=False):
    """
    从每个组合profile页面提取成员信息
    :param url: 各组合的profile网页 http://www.helloproject.com/morningmusume/profile/
    :return: {'name_en': 'mizuki_fukumura', 'name_jp': '譜久村聖', 'birthday': '1996/10/30', 'location': '東京都', 'group': 'morningmusume'}
    """
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    members = soup.select('#profile_memberlist > li > div')
    all_members = []
    for m in members:
        name_en = m.select('a')[0].get('href').split('/')[-2]
        # <a href="/morningmusume/profile/mizuki_fukumura/">
        name_jp = m.select('h4')[0].getText()
        birthday = m.select('dd')[0].getText()
        location = m.select('dd')[2].getText()
        group = url.split('/')[3]
        image_url = m.select('img')[0].get('src')

        member = dict(name_en=name_en, name_jp=name_jp, birthday=birthday, location=location, group=group)
        all_members.append(member)

        if download:
            # 下载当前成员照片
            download_picture(image_url, os.path.join('../images/helloproject', group), name_en + '.jpg')

    return all_members


def fetch_group_members(groups):
    """
    {'url': 'www.helloproject.com/morningmusume/profile', 'name_en': 'morningmusume', 'name_jp': "モーニング娘。'19"}
    :param groups: 各组合信息
    :return: 成员信息
    {'name_en': 'mizuki_fukumura', 'name_jp': '譜久村聖', 'birthday': '1996/10/30', 'location': '東京都', group': 'morningmusume'}
    """
    all_members = []
    for group in groups:
        members = members_from_profile(group['url'])
        all_members += members

    return all_members


def members_to_databases(members):
    """
    将成员信息保存到mongodb中
    :param members:{'name_en': 'mizuki_fukumura', 'name_jp': '譜久村聖', 'birthday': '1996/10/30', 'location': '東京都', 'group': 'morningmusume'}
    """
    client = pymongo.MongoClient(Mongodb_uri)
    my_db = client['helloproject']
    members_db = my_db['members']

    members_db.insert_many(members)


if __name__ == '__main__':
    # groups = fetch_artist_page()
    # # all_members = fetch_group_members(groups)
    # # members_to_databases(all_members)
    # group_to_database(groups)
    m1 = {
        'name_en': 'saki_shimizu',
        'name_jp': '清水佐紀',
        'birthday': '1991年11月22日',
        'location': '神奈川県',
        'group': 'berryzkobo'
    }
    m2 = {
        'name_en': 'momoko_tsugunaga',
        'name_jp': '嗣永桃子',
        'birthday': '1992年3月6日',
        'location': '千葉県',
        'group': 'berryzkobo'
    }
    m3 = {
        'name_en': 'chinami_tokunaga',
        'name_jp': '徳永千奈美',
        'birthday': '1992年5月22日',
        'location': '神奈川県',
        'group': 'berryzkobo'
    }

    m4 = {
        'name_en': 'maasa_sudou',
        'name_jp': '須藤茉麻',
        'birthday': '1992年7月3日',
        'location': '東京都',
        'group': 'berryzkobo'
    }

    m5 = {
        'name_en': 'miyabi_natsuyaki',
        'name_jp': '夏焼雅',
        'birthday': '1992年8月25日',
        'location': '千葉県',
        'group': 'berryzkobo'
    }
    m6 = {
        'name_en': 'yurina_kumai',
        'name_jp': '熊井友理奈',
        'birthday': '1993年8月3日',
        'location': '神奈川県',
        'group': 'berryzkobo'
    }

    m7= {
        'name_en': 'risako_sugaya',
        'name_jp': '菅谷梨沙子',
        'birthday': '1994年4月4日',
        'location': '神奈川県',
        'group': 'berryzkobo'
    }


    members_to_databases([m1, m2, m3, m4, m5, m6, m7])