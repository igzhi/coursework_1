import requests
import time
from datetime import date
from tqdm import tqdm

with open ('C:\\Users\\Igor & Alexa\\Desktop\\ИГОРЬ\\Нетология\\token_vk.txt', 'r') as f:
    token_vk = f.read()


def vk(vk_id, count):
    """Функция получает информацию из аккаунта VK по ID или screen_name"""

    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': f'{vk_id}',
        'access_token': f'{token_vk}',
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

def vk_id (vk_name):
    """Функция получает ID аккаунта VK по screen_name"""
    URL = 'https://api.vk.com/method/utils.resolveScreenName'
    params = {
        'screen_name': f'{vk_name}',
        'access_token': f'{token_vk}',
        'v': '5.131',
    }
    res = requests.get(URL, params=params)
    data = res.json()
    info = data['response']['object_id']
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
    vk_i = input('Чтобы найти пользователя VK введите "i" для поиска по ID или "n" для поиска по screen_name: ')

    if vk_i == 'i':
        vkid = input('Введите ID пользователя: ')
    else:
        vk_name = input('Введите screen_name пользователя: ')
        vkid = vk_id(vk_name)

    vk_count = input('Введите колличество необходимых фотографий: ')
    if not vk_count:
        vk_count = '5'

    vk_info = vk(vkid, vk_count)
    yandex_token = input('Введите token вашего Я.Диска: ')
    create_folder(yandex_token)
    names = []
    type_size = []
    for i in vk_info:
        url_y = i['sizes'][-1]['url']
        na = str(i['likes']['count'])
        type_s = i['sizes'][-1]['type']
        type_size.append(type_s)

        if na not in names:
            name_y = i['likes']['count']
            with open('json-файл.json', 'a') as file:
                file.write(f'file_name: {name_y}.jpg ')
        else:
            name_y = date.fromtimestamp(i['date'])
            with open('json-файл.json', 'a') as file:
                file.write(f'file_name: {name_y}.jpg ')
        names.append(str(i['likes']['count']))

        with open('json-файл.json', 'a') as file:
            file.write(f'size: {type_s} \n')

        upload_file(name_y, url_y, yandex_token)

    for _ in tqdm(vk_info):
        time.sleep(0.5)

if __name__ == "__main__":
    start()


