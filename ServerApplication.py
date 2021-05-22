from Aggregators.ShikimoriAggregator import ShikimoriAggregator
from UserSession import *


class ServerApplication:
    """Главный класс, который содержит сессии юзеров, агрегаторы"""
    def __init__(self):
        self.user_session = {}
        self.shikimori_anime_agg = ShikimoriAggregator()

    def get_user_session(self, user_id: int):
        """Получить сессию юзера"""
        if user_id not in self.user_session:
            self.user_session[user_id] = UserSession(user_id)
        return self.user_session[user_id]
