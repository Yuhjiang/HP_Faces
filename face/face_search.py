from face import client, my_db
from utils.image import image_to_base64
from config.config import image_path
import os
import time

images_db = my_db['images']
members_db = my_db['members']

# TODO 需要根据数据修改这里的代码


def face_multi_search(image, image_type, group_id_list='Hello_Project', save=False, match_threshold=70, max_face_num=10):
    """
    在图片里识别成员
    :param image: 从mongodb获取image数据
    :param image_type: BASE64 or URL
    :param group_id_list: 用户组，默认'Hello_Project'
    :param save: 是否保存到数据库
    :param match_threshold: 匹配阈值（设置阈值后，score低于此阈值的用户信息将不会返回）
    :param max_face_num: 最多处理人脸的数目
    :return:
    {'cached': 0,
 'error_code': 0,
 'error_msg': 'SUCCESS',
 'log_id': 1368654435158838371,
 'result': {'face_list': [{'face_token': 'bcd1d182ecc0b8e54ec2fbf9bae0d218',
                           'location': {'height': 301,
                                        'left': 5.17,
                                        'rotation': -19,
                                        'top': 234.03,
                                        'width': 308},
                           'user_list': [{'group_id': 'Hello_Project',
                                          'score': 90.319435119629,
                                          'user_id': 'ruru_dambara',
                                          'user_info': ''}]},
                          {'face_token': 'e9f9c20d6d8529cb07121d92b93a9340',
                           'location': {'height': 256,
                                        'left': 341.65,
                                        'rotation': 11,
                                        'top': 122.77,
                                        'width': 274},
                           'user_list': [{'group_id': 'Hello_Project',
                                          'score': 72.652542114258,
                                          'user_id': 'manaka_inaba',
                                          'user_info': ''}]}],
            'face_num': 2},
 'timestamp': 1563515883}
    """
    options = dict(match_threshold=match_threshold, max_face_num=max_face_num)
    if image_type == 'BASE64':
        img = image_to_base64(os.path.join(image_path, image['name']))
    else:
        img = image['url']
    try:
        res = client.multiSearch(img, image_type, group_id_list, options)
    except:
        res = {'error_msg': 'FAIL'}
    if save and res['error_msg'] == 'SUCCESS':
        face_to_databases(image, res)

    images_db.update(
        {'url': image['url']},
        {'$set': {'success': 1}}
    )
    return res


def face_to_databases(image, face):
    """
    将识别信息保存到数据库
    :param image: 从mongodb获取image数据
    :param face: face_multi_search()返回的数据
    """
    result = face['result']
    print(result)
    face_list = result['face_list']
    members = []
    for f in face_list:
        try:
            name_en = f['user_list'][0]['user_id']
            # 在members数据库找到相应成员
            member = members_db.find_one({'name_en': name_en})
            members.append({
                '_id': member['_id'],
                'name_en': member['name_en'],
                'name_jp': member['name_jp'],
                'group': member['group'],
            })
        except IndexError as e:
            pass

    members = {'$set': {'members': members, 'searched': 1}}
    query = {
        'url': image['url']
    }
    images_db.update_one(query, members)


def face_search():
    """
    识别所有图片
    :return:
    """
    face_to_search = images_db.find({'searched': 0, 'downloaded': 1, 'success': 0})
    for face in face_to_search:
        face_multi_search(face, 'BASE64', save=True)
        time.sleep(0.4)


if __name__ == '__main__':
    # image = images_db.find_one({'name': '785f6650gy1g54e5db3g7j20u00u0n95.jpg'})
    # res = face_multi_search(image, 'BASE64')
    # face_to_databases(image, res)
    face_search()