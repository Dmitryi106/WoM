import random


class Enemy():
    """Класс описывает вражеское существо"""

    def __init__(self, name):
        self.name = name
        self.health = 60
        self.attack = 12
        self.armor = 0

