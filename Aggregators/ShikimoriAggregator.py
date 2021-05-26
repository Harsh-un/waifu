from Aggregators.IAggregator import *
from config import *
import json
import requests


class ShikimoriItemFilter(IItemFilter):
    """Фильтр аниме (Shikimori)"""

    def __init__(self, genres: list = [], order: str = 'ranked', score: int = 1, rating: str = '',
                 kind: str = '', censored: str = 'true', name: str = "", page: int = 1, limit: int = 50):
        super().__init__()
        self.genres = genres
        self.order = order
        self.score = score
        self.rating = rating
        self.kind = kind
        self.censored = censored
        self.name = name
        self.page = page
        self.limit = limit


class ShikimoriItem(IItem):
    """Аниме (Shikimori)"""

    def __init__(self, name: str = '', genres: list = [], score: int = 0, description: str = '', image_url: str = '',
                 site_url: str = 'https://shikimori.one/', video_url: str = None):
        super().__init__()
        self.name = name
        self.genres = genres
        self.score = score
        self.description = description
        self.image_url = image_url
        self.site_url = site_url
        self.video_url = video_url


class ShikimoriAggregator(IAggregator):
    """Агрегатор (Shikimori)"""

    def __init__(self):
        super().__init__()
        self.site = CFG['aggregators']['shikimori']['site']
        self.client_id = CFG['aggregators']['shikimori']['auth']['client_id']
        self.client_secret = CFG['aggregators']['shikimori']['auth']['client_secret']
        self.authorization_code = CFG['aggregators']['shikimori']['auth']['authorization_code']
        with open(f'{MAIN_DIR}resources/ShikiToken.json', 'r') as file:
            data = json.load(file)
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']

    def get_name(self) -> str:
        return "Shikimori"

    def get_items(self, item_filter: ShikimoriItemFilter) -> AbstractItemIterator:
        """Получить итератор"""
        return ShikimoriItemIterator(self, item_filter)

    def get_new_token(self) -> None:
        new_token = requests.post(url=self.site + '/oauth/token',
                                  headers={
                                      "User-Agent": 'Telegram-Waifu'
                                  },
                                  data={
                                      'grant_type': 'refresh_token',
                                      'client_id': self.client_id,
                                      'client_secret': self.client_secret,
                                      'refresh_token': self.refresh_token
                                  }).json()
        self.access_token = new_token['access_token']
        self.refresh_token = new_token['refresh_token']
        with open(f'{MAIN_DIR}resources/ShikiToken.json', 'w') as file:
            json.dump(new_token, file, indent=2)
        return


class ShikimoriItemIterator(AbstractItemIterator):
    """Итератор (Shikimori)"""

    def __init__(self, shiki: ShikimoriAggregator, type_elem: TypeElem, item_filter: ShikimoriItemFilter):
        AbstractItemIterator.__init__(self)
        self.shiki = shiki
        self.type = type_elem
        self.item_filter = item_filter
        self.item_ids = []

    def get_item(self) -> ShikimoriItem:
        """Получить аниме по индексу"""
        if self.item_ids == []:
            self.item_ids = self.get_data_id()
        elif self.idx // 50 + 1 != self.item_filter.page:
            self.item_filter.page = self.idx // 50 + 1
            self.item_ids = self.get_data_id()

        if not (self.idx < len(self.item_ids)) or self.item_ids == []:
            return None

        # создание ссылки на запрос
        request_url = self.shiki.site
        if self.type is TypeElem.ANIME:
            request_url += '/api/animes/'
        elif self.type is TypeElem.MANGA:
            request_url += '/api/mangas/'
        request_url += str(self.item_ids[self.idx % 50])

        details = self.request_detailed(request_url)
        # Если токен невалидный, то получаем новый
        if details.status_code == 401:
            self.shiki.get_new_token()
            details = self.request_detailed(request_url)
        details = details.json()
        genres = []
        for genre in details['genres']:
            genres.append(genre['russian'])

        media_urls = None
        if self.type is TypeElem.ANIME:
            if details['licensors'] != []:
                media_urls = self.get_video_link([x.lower() for x in details['licensors']], request_url)
        elif self.type is TypeElem.MANGA:
            media_urls = self.get_manga_link(request_url)

        return ShikimoriItem(details['russian'], genres, details['score'],
                             details['description'], self.shiki.site + details['image']['original'],
                             self.shiki.site + details['url'], media_urls)

    def get_video_link(self, licensors: list, request_url: str) -> list:
        links = requests.get(url=request_url + '/external_links').json()
        result = []
        for link in links:
            if str.lower(link['kind']) in licensors:
                result.append((link['kind'], link['url']))
                break
        return result

    def get_manga_link(self, request_url: str) -> list:
        mangas = ['readmanga', 'mangalib', 'remanga', 'mangahub']
        links = requests.get(url=request_url + '/external_links').json()
        result = []
        for link in links:
            if link['kind'] in mangas:
                result.append((link['kind'], link['url']))
        return result if result != [] else None

    def get_data_id(self) -> list:
        request_url = self.shiki.site
        # запрос зависит от того что мы хотим найти
        if self.type is TypeElem.ANIME:
            request_url += '/api/animes'
        elif self.type is TypeElem.MANGA:
            request_url += '/api/mangas'

        dataset = self.request_items(request_url)
        # Если токен невалидный, то получаем новый
        if dataset.status_code == 401:
            self.shiki.get_new_token()
            dataset = self.request_items(request_url)
        dataset = dataset.json()

        # Сохраняем id аниме в список
        data_id = []
        for data in dataset:
            data_id.append(data['id'])
        return data_id

    def request_detailed(self, request_url: str) -> requests.Response:
        details = requests.get(url=request_url,
                               headers={
                                   "User-Agent": 'Telegram-Waifu',
                                   'Authorization': 'Bearer ' + self.shiki.access_token
                               })
        return details

    def request_items(self, request_url: str) -> requests.Response:
        datalist = requests.get(url=request_url,
                                headers={
                                    "User-Agent": 'Telegram-Waifu',
                                    'Authorization': 'Bearer ' + self.shiki.access_token
                                },
                                params={
                                    'page': self.item_filter.page,
                                    'limit': self.item_filter.limit,
                                    'order': self.item_filter.order,
                                    'score': self.item_filter.score,
                                    'rating': self.item_filter.rating,
                                    'kind': self.item_filter.kind,
                                    'genre': ','.join(self.item_filter.genres),
                                    'censored': self.item_filter.censored,
                                    'search': self.item_filter.name
                                })
        return datalist
