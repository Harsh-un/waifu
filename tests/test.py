from Aggregators.ShikimoriAggregator import *
from FavoriteItemList import AlreadyExistException
from ServerApplication import ServerApplication


app = ServerApplication()


def test_filter():
    """Проверка работы аггрегатора"""

    # объект аггрегатора
    agg = ShikimoriAggregator(app, TypeElem.ANIME)

    # объект фильтра, который заполняется через интерфейс телеги
    item_filter = ShikimoriItemFilter()

    # получение итератора аниме, чтобы проходится по ним вперед-назад
    item_iterator = agg.get_items(item_filter)

    # получение первого аниме
    item = item_iterator.get_item()

    # получение следующего аниме
    next_item = item_iterator.get_next_item()
    return

def test_search():
    # объект аггрегатора
    agg = ShikimoriAggregator(app, TypeElem.ANIME)

    # объект фильтра, который заполняется через интерфейс телеги
    item_filter = ShikimoriItemFilter(name='Берсерк')

    # получение итератора аниме, чтобы проходится по ним вперед-назад
    item_iterator = agg.get_items(item_filter)

    # получение аниме
    item, next_item = item_iterator.get_item(), item_iterator.get_next_item()
    return


def test_favor_list():
    agg = ShikimoriAggregator(app.db, TypeElem.ANIME)
    iter = agg.get_items(ShikimoriItemFilter(name='Берсерк'))

    user = app.get_user_session(1)

    item = iter.get_item()
    user.favorite_list.add_item(item)
    try:
        # добавляем точно такое же аниме в избранное и получаем ошибку
        user.favorite_list.add_item(item)
    except AlreadyExistException as ex:
        print('Уже существует в избранном.')
    # удаляем из списка избранного
    user.favorite_list.remove_item(item)
    return


def test_all():
    """Запуск всех тестов"""
    # Тест 1
    # test_filter()
    # Тест 2
    # test_search()

    # Тест 2
    test_favor_list()
    return


if __name__ == "__main__":
    test_all()

