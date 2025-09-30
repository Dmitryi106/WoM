import random


class Enemy():
    """Класс описывает вражеское существо"""

    def __init__(self, name):
        self.name = name
        self.health = 60
        self.attack = 12
        self.armor = 0

    def attacks(self):
        """Урон который будет наносить игрок"""
        return random.randint(self.attack - int((self.attack * 0.1)), self.attack + int((self.attack * 0.1)))