import requests
import time
import json
from datetime import date
from pprint import pprint
from tqdm import tqdm

def vk(vk_id, count):
    """Функция получает информацию из аккаунта VK"""
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': f'{vk_id}',
        'access_token': 'a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd',
        'v': '5.131',
        'album_id': 'profile',
        'extended': '1',
        'photo_sizes': '1',
        'count': f'{count}'
    }
    res = requests.get(URL, params=params)
    data = res.json()
    info = data['response']['items']
    return info

def create_folder(token):
    """Функция создает папку на Я.Диске"""
    upload_link = f'https://cloud-api.yandex.net:443/v1/disk/resources'
    header = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token}'}
    params = {'path': f'Сoursework', 'overwrite': True}
    requests.put(upload_link, params=params, headers=header)

def upload_file(name1, url2, token):
    """Функция сохраняет фотографии на Я.Диске"""
    upload_link = f'https://cloud-api.yandex.net:443/v1/disk/resources/upload/'
    header = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token}'}
    params = {'path': f'Сoursework/{name1}.jpg','url': url2, 'overwrite': True}
    requests.post(upload_link, params=params, headers=header)

def start():
    vk_id = input('Введите id пользователя в ВКонтакте: ')
    vk_count = input('Введите колличество необходимых фотографий: ')
    if not vk_count:
        vk_count = '5'
    vk_info = vk(vk_id, vk_count)
    yandex_token = input('Введите token вашего Я.Диска: ')
    create_folder(yandex_token)
    names = []
    for i in vk_info:
        url_y = i['sizes'][-1]['url']
        na = str(i['likes']['count'])

        if na not in names:
            name_y = i['likes']['count']
        else:
            name_y = date.fromtimestamp(i['date'])
        names.append(str(i['likes']['count']))

        upload_file(name_y, url_y, yandex_token)

    for q in tqdm(names):
        time.sleep(1)

start()


