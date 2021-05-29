from IItem import IItem


class IItemMapper:
    """Маппер"""
    def __init__(self):
        pass

    def find_by_id(self, item_id: int) -> IItem:
        """Найти аниме в БД по ид"""
        pass

    def add_item(self, item: IItem):
        """Добавить аниме в БД"""
        pass

    def remove_item(self, item: IItem):
        """Удалить аниме из БД"""
        pass
