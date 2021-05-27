from Aggregators.IAggregator import *
import UserSession


class AlreadyExistException(Exception):
    """Исключение"""
    def __init__(self):
        super().__init__("Объект уже в избранном.")


class FavoriteItem:
    """Аниме или манга"""
    def __init__(self, user: UserSession, item_id: int, name: str):
        self.user = user
        self.item_id = item_id
        self.name = name


class FavoriteItemList:
    """Список избранного"""
    def __init__(self, user: UserSession, db):
        super().__init__()
        self.user = user
        self.db = db
        self.item_list = []

    def get_favor_items(self):
        """Получить список аниме"""
        return self.item_list

    def load(self):
        """Загрузка аниме из БД"""
        cursor = self.db.cursor()
        cursor.execute("SELECT item_id, name FROM favorite_items WHERE user_id = ?", self.user.user_id)
        for row in cursor.fetchall():
            self.item_list.append(FavoriteItem(self.user, row['item_id'], row['name']))
        return

    def add_item(self, item: IItem):
        """Добавить аниме в избранное"""
        # проверка на то, что объект уже в избранном
        for favor_item in self.item_list:
            if favor_item.item_id == item.get_id():
                raise AlreadyExistException()

        self.item_list.append(FavoriteItem(self.user, item.get_id(), item.get_name()))
        cursor = self.db.cursor()
        cursor.execute("INSERT INTO favorite_items (user_id, item_id, name) VALUES (?, ?, ?)",
                       (self.user.user_id, item.get_id(), item.get_name()))
        self.db.commit()
        return

    def remove_item(self, item: IItem):
        """Удалить аниме из избранного"""
        self.item_list = list(filter(lambda x: x.item_id != item.get_id(), self.item_list))
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM favorite_items WHERE user_id=? AND item_id=?",
                       (self.user.user_id, item.get_id()))
        self.db.commit()
        return
