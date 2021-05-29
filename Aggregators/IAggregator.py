from AbstractItemIterator import AbstractItemIterator
from IItemMapper import IItemMapper


class IItemFilter:
    """Фильтр формируется путем нажатия определенных кнопок"""

    def __init__(self):
        pass


class IAggregator:
    """Агрегатор"""

    def __init__(self):
        pass

    def get_mapper(self) -> IItemMapper:
        """Mapper"""
        pass

    def get_id(self) -> int:
        """ID"""
        pass

    def get_name(self) -> str:
        """Название"""
        pass

    def get_items(self, item_filter: IItemFilter) -> AbstractItemIterator:
        """Получить итератор"""
        pass
