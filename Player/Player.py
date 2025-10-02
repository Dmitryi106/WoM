import random

class Player():
    """Класс описывает игрока"""

    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack = 10
        self.armor = 0
        self.level = 1
        self.gold = 0
        self.exp = 0
        self.exp_to_level = 50

    def is_alive(self):
        if self.health <= 0:
            print("Вы погибли!")
            return False
        return True


