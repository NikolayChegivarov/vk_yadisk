import requests
import vk_api
import json
from tqdm import tqdm
import time

def vk_yandex(vk_id, yandex_token):

    # получаю массив объектов фотографий
    token = ''  # token vk program
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()
    photos = vk.photos.get(owner_id=vk_id, album_id='profile', extended=1, count=10)

    # записываю нужные фото в словарь
    photo_yandex = {}
    output = []
    for i in photos['items']:
        file = {}

        likes_count = str(i['likes']['count'])  # Получаю количество лайков
        # max_type_url = max(i['sizes'], key=lambda size: size['type'])['url']  # URL максимального размера
        max_type_url = i['sizes'][-1]['url']  # URL максимального размера через индекс
        date_ = i['date']  # Получаю дату
        if likes_count in photo_yandex:
            photo_yandex[likes_count + str(date_)] = max_type_url
            file = {"file_name": f'{likes_count + str(date_)}.jpg',
                    "size": i['sizes'][-1]['type']}
            output.append(file)
        else:
            photo_yandex[likes_count] = max_type_url
            file = {"file_name": f'{likes_count}.jpg',
                    "size": i['sizes'][-1]['type']}
            output.append(file)

    # Записываю json-файл с информацией по файлам
    with open('data.json', 'w') as f:
        json.dump(output, f)

    # создаю папку на яндекс диске
    headers = {"Authorization": f"OAuth {yandex_token}"}
    params = {"path": "/photo vk"}
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    response = requests.put(url, headers=headers, params=params)
    if response.status_code == 201:
        print("Папка успешно создана")
    else:
        print("Ошибка при создании папки. Статус код:", response.status_code)

    # загружаю фото на яндекс диск
    for name, url in tqdm(photo_yandex.items(), ascii=True, desc='Netology only love'):
        time.sleep(1)
        params = {
        'url':url,  # сюда интегрирую прогресс бар
        'path':f'photo vk/{name}',  # ТАКОФФ ПУТЬ.
        'fields':name
        }
        response_ = requests.post(
            f'https://cloud-api.yandex.net/v1/disk/resources/upload?', params=params,
            headers=headers)


vk_yandex('', '')