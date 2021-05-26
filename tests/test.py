from Aggregators.ShikimoriAggregator import *

def test_filter():
    """Проверка работы аггрегатора"""

    # объект аггрегатора
    agg = ShikimoriAggregator(TypeElem.ANIME)

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
    agg = ShikimoriAggregator(TypeElem.ANIME)

    # объект фильтра, который заполняется через интерфейс телеги
    item_filter = ShikimoriItemFilter(name='Берсерк')

    # получение итератора аниме, чтобы проходится по ним вперед-назад
    item_iterator = agg.get_items(item_filter)

    # получение аниме
    item, next_item = item_iterator.get_item(), item_iterator.get_next_item()
    return

def test_all():
    """Запуск всех тестов"""
    # Тест 1
    test_filter()
    # Тест 2
    test_search()
    return


if __name__ == "__main__":
    test_all()

