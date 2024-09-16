# -*- coding: utf-8 -*-
from transformers import pipeline
import requests
import json
import datetime
import time
from summ import sum


#получает id группы
def get_Group_Id(url):
    # переменные
    TOKEN_USER = '24d069d124d069d124d069d10127c7109d224d024d069d14137222378bc8977bd373a52'
    VERSION = 5.199
    DOMAIN = url

    response = requests.get('https://api.vk.com/method/utils.resolveScreenName',
                            params={
                                'access_token': TOKEN_USER,
                                'v': VERSION,
                                'screen_name': DOMAIN,

                            })


    group_id = response.json()['response']['object_id']

    return group_id * -1


#получает все посты с группы
def get_Posts(url,count, offset = 0):
    # переменные
    TOKEN_USER = '24d069d124d069d124d069d10127c7109d224d024d069d14137222378bc8977bd373a52'
    VERSION = 5.199
    DOMAIN = url
    COUNT = count
    OFFSET = offset
    # через api vk вызываем статистику постов
    response = requests.get('https://api.vk.com/method/wall.get',
    params={'access_token': TOKEN_USER,
            'v': VERSION,
            'domain': DOMAIN,
            'count': COUNT,
            'offset' : OFFSET
            })

    data = response.json()['response']['items']
    return data

#возвращает комменты опеределенного поста
def get_Comments(url,post_id,count):
    # переменные
    TOKEN_USER = '24d069d124d069d124d069d10127c7109d224d024d069d14137222378bc8977bd373a52'
    VERSION = 5.199
    GROUP_ID = get_Group_Id(url)
    COMMENTS_COUNT = count
    all_comments = []

    response = requests.get('https://api.vk.com/method/wall.getComments',
                            params={'access_token': TOKEN_USER,
                                    'v': VERSION,
                                    'owner_id': GROUP_ID,
                                    'post_id' : post_id,
                                    'count': COMMENTS_COUNT
                                    })

    comments = response.json()['response']['items']

    for comment in comments :
        all_comments.append(comment['text'])


        if(comment['thread']['count'] != 0 ):
            all_comments += get_subcomments(comment['id'],GROUP_ID,post_id)
            time.sleep(0.1)

    return all_comments

#получает ветку комментво определнного коммента
def get_subcomments(comment_id,group_id,post_id ):
    TOKEN_USER = '24d069d124d069d124d069d10127c7109d224d024d069d14137222378bc8977bd373a52'
    VERSION = 5.199

    all_subcomments = []


    response = requests.get('https://api.vk.com/method/wall.getComments',
                            params={'access_token': TOKEN_USER,
                                    'v': VERSION,
                                    'owner_id': group_id,
                                    'post_id': post_id,
                                    'comment_id' : comment_id
                                    })

    data = response.json()['response']['items']

    for d in data:
        all_subcomments.append(d['text'])


    return all_subcomments

#https://vk.com/psu_community?w=wall-206949619_645
#получает словарь постов - комментов
def get_All(name,count):
    all_posts = []
    all_text = {}
    offset = 0
    # надо закинуть в функцию наверное , получает все посты по count
    while count > 100 :
        #получаем посты
        posts = get_Posts(name,count,offset=offset)
        all_posts += posts
        count -= 100
        offset += 100

    all_posts += get_Posts(name,count,offset=offset)


    for post in all_posts:
        post_url = f'https://vk.com/{name}?w=wall{post["owner_id"]}_{post["id"]}'
        post_date = datetime.datetime.fromtimestamp(int(post['date']))
        text = sum(post['text'])
        comments = get_Comments(name, post['id'], post['comments']['count'])
        all_text['Пост'] = text
        all_text['Комментарии'] = comments
        all_text['оценка'] = 'нейтральная'
        all_text['ссылка'] = post_url

        #all_text[text] = get_Comments(name, post['id'], post['comments']['count'])

        time.sleep(0.1)

    return all_text

    All_text = get_All('psu_community', 5)

    print(All_text)