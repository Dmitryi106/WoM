import json
import os

class Enemy:
    """Класс описывает врага, загружая данные из Enemy_classes.json"""

    def __init__(self, enemy_id: str):
        # Получаем путь к файлу классов врагов относительно текущего файла
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "..", "Classes_game", "Enemy_classes.json")
        file_path = os.path.normpath(file_path)

        # Проверяем существование файла
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл классов врагов не найден: {file_path}")

        # Загружаем данные
        with open(file_path, "r", encoding="utf-8") as f:
            enemies_data = json.load(f)

        if enemy_id not in enemies_data:
            raise ValueError(f"Враг с ID {enemy_id} не найден в {file_path}")

        data = enemies_data[enemy_id]
        self.name = data["name"]
        self.health = data["health"]
        self.max_health = data["health"]
        self.attack = data["attack"]
        self.armor = data["armor"]
        self.level = data["level"]
        self.reward_exp = data["reward_exp"]

        # Дополнительные свойства (если есть)
        self.spell_power = data.get("spell_power", 0)
        self.poison_damage = data.get("poison_damage", 0)
        self.fire_damage = data.get("fire_damage", 0)
        self.ice_damage = data.get("ice_damage", 0)
        self.crit_chance = data.get("crit_chance", 0)
        self.dodge_chance = data.get("dodge_chance", 0)
        self.curse_damage = data.get("curse_damage", 0)
        self.divine_damage = data.get("divine_damage", 0)
        self.range_attack = data.get("range_attack", 0)
        self.eye_laser = data.get("eye_laser", 0)

    def is_alive(self):
        """Проверяет, жив ли враг."""
        return self.health > 0

    def take_damage(self, damage):
        """Наносит урон по врагу с учётом брони."""
        reduced_damage = max(1, damage - self.armor)  # Урон не может быть меньше 1
        self.health -= reduced_damage
        print(f"{self.name} получил {reduced_damage} урона. Осталось здоровья: {self.health}")
        if not self.is_alive():
            print(f"{self.name} повержен!")

    def __str__(self):
        return (f"{self.name} (Ур. {self.level}) — Здоровье: {self.health}, Атака: {self.attack}, "
                f"Броня: {self.armor}, Награда: {self.reward_exp} опыта")