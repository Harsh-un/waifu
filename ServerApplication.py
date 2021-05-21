from UserSession import *


class ServerApplication:
    """Содержит сессии юзеров, агрегаторы (анимэ, манга)"""
    def __init__(self):
        self.user_session = {}

    def get_user_session(self, user_id: int):
        """Получить сессию юзера"""
        if user_id not in self.user_session:
            self.user_session[user_id] = UserSession()
        return self.user_session[user_id]