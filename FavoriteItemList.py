import sqlite3
from contextlib import closing
import UserSession
from IItem import IItem
from config import *


class AlreadyExistException(Exception):
    """Исключение"""
    def __init__(self):
        super().__init__("Объект уже в избранном.")


class FavoriteItemList:
    """Список избранного"""
    def __init__(self, user: UserSession, app):
        super().__init__()
        self.user = user
        self.app = app
        self.item_list = []

    def get_items(self):
        """Получить список аниме"""
        return self.item_list

    def load(self):
        """Загрузка аниме из БД"""
        with closing(sqlite3.connect(MAIN_DIR + CFG['db_file'])) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT agg_id, item_id FROM favorite_items WHERE user_id = ?", [self.user.user_id])
            for row in cursor.fetchall():
                agg = self.app.get_agg_by_id(row[0])
                item = agg.get_mapper().find_by_id(row[1])
                if item is not None:
                    self.item_list.append(item)
        return

    def add_item(self, item: IItem):
        """Добавить аниме в избранное"""
        # проверка на то, что объект уже в избранном
        for favor_item in self.item_list:
            if favor_item.get_id() == item.get_id():
                raise AlreadyExistException()

        with closing(sqlite3.connect(MAIN_DIR + CFG['db_file'])) as conn:
            self.item_list.append(item)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO favorite_items (user_id, agg_id, item_id) VALUES (?, ?, ?)",
                           (self.user.user_id, item.get_agg().get_id(), item.get_id()))
            conn.commit()
        return

    def remove_item(self, item: IItem):
        """Удалить аниме из избранного"""
        with closing(sqlite3.connect(MAIN_DIR + CFG['db_file'])) as conn:
            self.item_list = list(filter(lambda x: x.item_id != item.get_id(), self.item_list))
            cursor = conn.cursor()
            cursor.execute("DELETE FROM favorite_items WHERE agg_id=? AND item_id=?",
                           (item.get_agg().get_id(), item.get_id()))
            conn.commit()
        return
