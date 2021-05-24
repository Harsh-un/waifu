from Aggregators.ShikimoriAggregator import *
from ServerApplication import ServerApplication


def test_shikimori_aggregator():
    """Проверка работы аггрегатора"""

    # объект аггрегатора
    agg = ShikimoriAggregator()

    # объект фильтра, который заполняется через интерфейс телеги
    item_filter = ShikimoriItemFilter()

    # получение итератора аниме, чтобы проходится по ним вперед-назад
    item_iterator = agg.get_items(item_filter)

    # получение первого аниме
    item = item_iterator.get_item(0)

    # получение следующего аниме
    next_item = item_iterator.get_next_item()
    return


def test_all():
    """Запуск всех тестов"""
    test_shikimori_aggregator()
    return


if __name__ == "__main__":
    test_all()

