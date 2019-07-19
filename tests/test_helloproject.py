"""
测试helloproject模块
"""

import unittest
import pymongo
from config.config import Mongodb_uri
from helloproject.helloproject import (fetch_artist_page,
                                       group_to_database,
                                       members_from_profile,
                                       fetch_group_members,
                                       members_to_databases,
                                       )


class TestHelloProject(unittest.TestCase):
    def setUp(self):
        client = pymongo.MongoClient(Mongodb_uri)
        my_db = client['helloproject']
        collections = my_db.list_collection_names()
        # 判断是否存在 groups
        if 'groups' in collections:
            groups = my_db['groups']
            groups.drop()
        if 'members' in collections:
            members = my_db['members']
            members.drop()
        client.close()

    @unittest.skip
    def test_fetch_artist_page(self):
        url = 'http://www.helloproject.com/artist/'

        res = fetch_artist_page(url)
        result = [
            {'url': 'http://www.helloproject.com/morningmusume/profile', 'name_en': 'morningmusume', 'name_jp': "モーニング娘。'19"},
            {'url': 'http://www.helloproject.com/angerme/profile', 'name_en': 'angerme', 'name_jp': 'アンジュルム'},
            {'url': 'http://www.helloproject.com/juicejuice/profile', 'name_en': 'juicejuice', 'name_jp': 'Juice=Juice'},
            {'url': 'http://www.helloproject.com/countrygirls/profile', 'name_en': 'countrygirls', 'name_jp': 'カントリー・ガールズ'},
            {'url': 'http://www.helloproject.com/kobushifactory/profile', 'name_en': 'kobushifactory', 'name_jp': 'こぶしファクトリー'},
            {'url': 'http://www.helloproject.com/tsubakifactory/profile', 'name_en': 'tsubakifactory', 'name_jp': 'つばきファクトリー'},
            {'url': 'http://www.helloproject.com/beyooooonds/profile', 'name_en': 'beyooooonds', 'name_jp': 'BEYOOOOONDS'},
            {'url': 'http://www.helloproject.com/helloprokenshusei/profile', 'name_en': 'helloprokenshusei', 'name_jp': 'ハロプロ研修生'},
            {'url': 'http://www.helloproject.com/helloprokenshuseihokkaido/profile', 'name_en': 'helloprokenshuseihokkaido', 'name_jp': 'ハロプロ研修生北海道'}
        ]

        self.assertEqual(res, result)

    @unittest.skip
    def test_group_to_database(self):
        groups = fetch_artist_page()
        group_to_database(groups)
        client = pymongo.MongoClient(Mongodb_uri)
        my_db = client['helloproject']
        groups = my_db['groups']
        group = groups.find_one({'name_en': 'morningmusume'})
        self.assertTrue(group is not None)

    @unittest.skip
    def test_members_from_profile(self):
        url = 'http://www.helloproject.com/morningmusume/profile/'
        all_members = members_from_profile(url)
        result = {'name_en': 'mizuki_fukumura', 'name_jp': '譜久村聖', 'birthday': '1996年10月30日', 'location': '東京都', 'group': 'morningmusume'}

        self.assertTrue(all_members[0] == result)

    @unittest.skip
    def test_fetch_group_members(self):
        groups = fetch_artist_page('http://www.helloproject.com/artist/')
        all_members = fetch_group_members(groups)
        result = {'name_en': 'mizuki_fukumura', 'name_jp': '譜久村聖', 'birthday': '1996年10月30日', 'location': '東京都', 'group': 'morningmusume'}

        self.assertTrue(all_members[0] == result)

    @unittest.skip
    def test_members_to_databases(self):
        groups = fetch_artist_page()
        all_members = fetch_group_members(groups)
        members_to_databases(all_members)

        client = pymongo.MongoClient(Mongodb_uri)
        my_db = client['helloproject']
        members_db = my_db['members']

        member = members_db.find_one()
        self.assertTrue(member is not None)