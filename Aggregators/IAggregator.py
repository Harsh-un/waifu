from IItem import IItem
from IItemMapper import IItemMapper


class IItemFilter:
    """Фильтр формируется путем нажатия определенных кнопок"""
    def __init__(self):
        pass


class AbstractItemIterator:
    """Итератор, который на ходу подгружает аниме"""
    def __init__(self):
        self.idx = 0

    def get_next_item(self) -> IItem:
        """Следующий"""
        self.idx += 1
        return self.get_item()

    def get_prev_item(self) -> IItem:
        """Предыдущий"""
        if self.idx != 0:
            self.idx -= 1
        return self.get_item()

    def empty(self) -> bool:
        """Пустой ли итератор"""
        return self.get_item() is None

    def get_item(self) -> IItem:
        """Получить item по индексу"""
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
