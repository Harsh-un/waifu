import sqlite3
from Aggregators.ShikimoriAggregator import *
from UserSession import *


class ServerApplication:
    """Главный класс, который содержит сессии юзеров, агрегаторы"""

    def __init__(self):
        self.user_session = {}
        self.shikimori_anime_agg = ShikimoriAggregator(TypeElem.ANIME)
        self.shikimori_manga_agg = ShikimoriAggregator(TypeElem.MANGA)

    def get_agg_by_id(self, id: int) -> IAggregator:
        if id == self.shikimori_anime_agg.get_id():
            return self.shikimori_anime_agg
        return self.shikimori_manga_agg

    def get_user_session(self, user_id: int):
        """Получить сессию юзера"""
        if user_id not in self.user_session:
            user = UserSession(user_id)
            self.user_session[user_id] = user
            user.favorite_list = FavoriteItemList.FavoriteItemList(user, self)
            user.favorite_list.load()
        return self.user_session[user_id]
