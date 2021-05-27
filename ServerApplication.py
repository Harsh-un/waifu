import sqlite3
from Aggregators.ShikimoriAggregator import *
from UserSession import *


class ServerApplication:
    """Главный класс, который содержит сессии юзеров, агрегаторы"""
    def __init__(self):
        self.user_session = {}
        self.shikimori_anime_agg = ShikimoriAggregator(TypeElem.ANIME)
        self.shikimori_manga_agg = ShikimoriAggregator(TypeElem.MANGA)
        self.db_init()

    def db_init(self):
        self.db = sqlite3.connect(MAIN_DIR + CFG['db_file'])

    def get_user_session(self, user_id: int):
        """Получить сессию юзера"""
        if user_id not in self.user_session:
            self.user_session[user_id] = UserSession(user_id, self.db)
        return self.user_session[user_id]
