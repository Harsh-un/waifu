import FavoriteItemList


class UserSession:
    """Харнит всю требуемую информацию об одном юзере в течение сессии"""
    def __init__(self, user_id: int, db):
        self.user_id = user_id
        self.cur_aggregator = None
        self.cur_filter = None
        self.cur_iterator = None
        self.cur_type = None
        self.favorite_list = FavoriteItemList.FavoriteItemList(self, db)
