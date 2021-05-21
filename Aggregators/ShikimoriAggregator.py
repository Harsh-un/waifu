from Aggregators.IAggregator import *


class ShikimoriItemFilter(IItemFilter):
    """Фильтр анимэ (Shikimori)"""
    def __init__(self, genres: list, order: str, score: int, rating: str, censored: bool, name: str):
        self.genres = genres
        self.order = order
        self.score = score
        self.rating = rating
        self.censored = censored
        self.name = name


class ShikimoriItem(IItem):
    """Анимэ (Shikimori)"""
    def __init__(self, name: str, genres: list, score: int, description: str, image_url: str):
        self.name = name
        self.genres = genres
        self.score = score
        self.description = description
        self.image_url = image_url


class ShikimoriItemIterator(AbstractItemIterator):
    """Итератор (Shikimori)"""
    def __init__(self, item_filter: ShikimoriItemFilter):
        AbstractItemIterator.__init__(self, item_filter)
        self.item_ids = []

    def get_item(self, idx: int) -> IItem:
        """Получить анимэ по индексу"""
        pass


class ShikimoriAggregator(IAggregator):
    """Агрегатор (Shikimori)"""
    def __init__(self):
        pass

    def get_name(self) -> str:
        return "Shikimori"

    def get_items(self, item_filter: ShikimoriItemFilter) -> AbstractItemIterator:
        """Получить итератор"""
        return ShikimoriItemIterator(item_filter)