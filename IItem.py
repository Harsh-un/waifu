# from Aggregators.IAggregator import IAggregator


class IItem:
    """Анимэ/Манга"""

    def __init__(self):
        pass

    def get_agg(self):
        """Агрегатор"""
        pass

    def get_name(self) -> str:
        """Название"""
        pass

    def get_id(self) -> int:
        """ID"""
        pass
