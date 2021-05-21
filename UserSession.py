from Aggregators.IAggregator import AbstractItemIterator


class UserSession:
    """Харнит всю требуемую информацию об одном юзере"""
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.cur_iterator = None
