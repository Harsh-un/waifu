import sqlite3
from Aggregators.ShikimoriAggregator import *
from UserSession import *


class ServerApplication:
    """Главный класс, который содержит сессии юзеров, агрегаторы"""
    def __init__(self):
        self.db_init()
        self.user_session = {}
        self.shikimori_anime_agg = ShikimoriAggregator(self.db, TypeElem.ANIME)
        self.shikimori_manga_agg = ShikimoriAggregator(self.db, TypeElem.MANGA)

    def get_agg_by_id(self, id: int) -> IAggregator:
        if id == self.shikimori_anime_agg.get_id():
            return self.shikimori_anime_agg
        return self.shikimori_manga_agg

    def db_init(self):
        self.db = sqlite3.connect(MAIN_DIR + CFG['db_file'])

    def get_user_session(self, user_id: int):
        """Получить сессию юзера"""
        if user_id not in self.user_session:
            self.user_session[user_id] = UserSession(user_id, self.db)
        return self.user_session[user_id]
