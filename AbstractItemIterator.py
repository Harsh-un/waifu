from IItem import IItem


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

    def has_prev(self) -> bool:
        """prev"""
        return self.idx > 0

    def has_next(self) -> bool:
        """next"""
        pass

    def get_item(self) -> IItem:
        """Получить item по индексу"""
        pass
