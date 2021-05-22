import requests
import json

site = 'https://shikimori.one'
client_id = 'P4VOYDWfWYQlhhFRqS8sONg39LAgHGHLRSTMU_1PMeM'
client_secret = 'wno6Ij5zaplABAMFO1exSBQ2VCEY0pBEMJsQStKpr8M'
authorization_code = 'rPXm12xqS9ygdnO438i4kI9iCBDmdGLLK5IaPKas5Iw'
access_token = ''
refresh_token = ''
# https://shikimori.one/api/animes?limit=2&order=ranked

with open('resources/ShikiToken.json', 'r') as file:
    data = json.load(file)
    global access_token
    global refresh_token
    access_token = data['access_token']
    refresh_token = data['refresh_token']

headers_for_request = {
    "User-Agent": 'Telegram-Waifu',
    'Authorization': 'Bearer ' + access_token
}
data_for_request = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'client_secret': client_secret,
    'code': authorization_code,
    'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'
}

# Хранит id аниме для каждого пользователя
store_users_anime_id = dict()


# genres-список индентификаторов жанров ОБЯЗАТЕЛЬНО
def get_anime_id_list(genres, page=1, limit=50, order='ranked', score=1, rating='none', censored='true', name=''):
    parametrs = {
        'page': page,
        'limit': limit,
        'order': order,
        'score': score,
        'rating': rating,
        'genre': genres,
        'censored': censored,
        'search': name
    }
    animes = requests.get(url=site + '/api/animes', headers=headers_for_request, params=parametrs)
    # Если токен невалидный, то получаем новый
    if animes.status_code == 401:
        get_new_access_token()
        animes = requests.get(url=site + '/api/animes', headers=headers_for_request, params=parametrs)
    animes = animes.json()

    # Сохраняем id аниме в список
    animes_id = []
    for anime in animes:
        animes_id.append(anime['id'])
    return animes_id


# type - tv, movie
def get_anime(user_id, type, genres, num_anime=0, name='', rating='none'):
    global store_users_anime_id
    if user_id not in store_users_anime_id:
        store_users_anime_id[user_id] = {
            'animes': get_anime_id_list(type=type, genres=genres, name=name, rating=rating),
            'page': num_anime % 50 + 1
        }
    elif num_anime % 50 + 1 > store_users_anime_id[user_id]['page']:
        store_users_anime_id[user_id]['page'] = num_anime % 50 + 1
        store_users_anime_id[user_id]['animes'] = get_anime_id_list(type=type, genres=genres,
                                                                    page=store_users_anime_id[user_id]['page'],
                                                                    name=name, rating=rating)
    elif num_anime % 50 + 1 < store_users_anime_id[user_id]['page']:
        store_users_anime_id[user_id]['page'] = num_anime % 50 + 1
        store_users_anime_id[user_id]['animes'] = get_anime_id_list(type=type, genres=genres,
                                                                    page=store_users_anime_id[user_id]['page'],
                                                                    name=name, rating=rating)

    # получение id аниме
    anime_id = store_users_anime_id[user_id]['animes'][num_anime]

    # Получение подробной информации об определенном аниме по id
    anime_info = requests.get(url=site + '/api/animes/' + str(anime_id),
                              headers=headers_for_request
                              )

    # Если токен не валидный, то получаем новый
    if anime_info.status_code == 401:
        get_new_access_token()
        anime_info = requests.get(url=site + '/api/animes/' + str(anime_id),
                                  headers=headers_for_request,
                                  )

    message = data_for_message(anime_info.json())
    return message  # (name, genres, score, description, image)


def get_new_access_token():
    global access_token
    global refresh_token
    headers_for_get_token = {
        "User-Agent": 'Telegram-Waifu'
    }
    data_for_get_refresh_token = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    new_tokens = requests.post(url=site + '/oauth/token', headers=headers_for_get_token,
                               data=data_for_get_refresh_token).json()

    access_token = new_tokens['access_token']
    refresh_token = new_tokens['refresh_token']
    with open('resources/ShikiToken.json', 'w') as jsfile:
        json.dump(new_tokens, jsfile, indent=2)
    return


def data_for_message(anime_info):
    name = anime_info['russian']
    score = anime_info['score']
    description = anime_info['description']
    image = site + anime_info['image']['original']
    genres = ''
    for genre in anime_info['genres']:
        genres += genre['russian'] + ', '
    genres = genres[:-2]
    return (name, genres, score, description, image)


def delete_info_users(user_id):
    del store_users_anime_id[user_id]
