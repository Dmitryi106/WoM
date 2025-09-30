import random

class Player():
    """Класс описывает игрока"""

    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack = 10
        self.armor = 0

    def attacks(self):
        """Урон который будет наносить игрок"""
        return random.randint(self.attack - int((self.attack * 0.1)),self.attack + int((self.attack * 0.1)))
