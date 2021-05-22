from Aggregators.IAggregator import *


class ShikimoriItemFilter(IItemFilter):
    """Фильтр аниме (Shikimori)"""
    def __init__(self, genres: list = [], order: str = 'random', score: int = 0, rating: str = 'none',
                 censored: bool = True, name: str = ""):
        super().__init__()
        self.genres = genres
        self.order = order
        self.score = score
        self.rating = rating
        self.censored = censored
        self.name = name


class ShikimoriItem(IItem):
    """Аниме (Shikimori)"""
    def __init__(self, name: str = '', genres: list = [], score: int = 0, description: str = '', image_url: str = ''):
        super().__init__()
        self.name = name
        self.genres = genres
        self.score = score
        self.description = description
        self.image_url = image_url


class ShikimoriItemIterator(AbstractItemIterator):
    """Итератор (Shikimori)"""
    def __init__(self, item_filter: ShikimoriItemFilter):
        AbstractItemIterator.__init__(self)
        self.item_filter = item_filter
        self.item_ids = []

    def get_item(self, idx: int) -> IItem:
        """Получить анимэ по индексу"""
        pass


class ShikimoriAggregator(IAggregator):
    """Агрегатор (Shikimori)"""
    def __init__(self):
        super().__init__()

    def get_name(self) -> str:
        return "Shikimori"

    def get_items(self, item_filter: ShikimoriItemFilter) -> AbstractItemIterator:
        """Получить итератор"""
        return ShikimoriItemIterator(item_filter)
