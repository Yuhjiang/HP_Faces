"""
处理www.helloproject.com页面的模块
1. 收集成员信息
"""


import requests
import bs4
import pymongo
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


def members_from_profile(url):
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

        member = dict(name_en=name_en, name_jp=name_jp, birthday=birthday, location=location, group=group)
        all_members.append(member)

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