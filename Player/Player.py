import json
import os
import random


class Player:
    """Класс описывает игрока, загружая данные из Player_classes.json"""

    def __init__(self, class_id: str, name: str = "Игрок"):
        # Получаем путь относительно текущего файла
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "..", "Classes_game", "Player_classes.json")
        file_path = os.path.normpath(file_path)  # нормализуем путь

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл классов не найден: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            classes_data = json.load(f)

        if class_id not in classes_data:
            raise ValueError(f"Класс с ID {class_id} не найден в {file_path}")

        data = classes_data[class_id]
        self.max_health = data["health"]
        self.name = name
        self.class_name = data["name"]
        self.health = data["health"]
        self.max_health = data["health"]
        self.attack = data["attack"]
        self.armor = data["armor"]
        self.level = 1
        self.gold = 50
        self.exp = 0
        self.exp_to_next = 100

        # Новые свойства
        self.crit_chance = data.get("crit_chance", 0.1)  # По умолчанию 10%
        self.spell_power = data.get("spell_power", 0)
        self.mana = 100
        self.max_mana = 100

        # Скиллы
        self.skills = []

        # Инвентарь
        self.inventory = {
            "health_potion": 2,  # Зелья здоровья
            "mana_potion": 1  # Зелья маны
        }
        # Загружаем скиллы из JSON
        self.load_skills()

    def load_skills(self):
        """Загружает базу скиллов из JSON"""
        current_dir = os.path.dirname(__file__)
        skills_file = os.path.join(current_dir, "..", "Classes_game", "Skills.json")
        skills_file = os.path.normpath(skills_file)

        if not os.path.exists(skills_file):
            raise FileNotFoundError(f"Файл скиллов не найден: {skills_file}")

        with open(skills_file, "r", encoding="utf-8") as f:
            self.skills_db = json.load(f)

    def is_alive(self):
        if self.health <= 0:
            print("Вы погибли!")
            return False
        return True

    def add_exp(self, amount):
        self.exp += amount
        print(f"Получено {amount} опыта. Всего: {self.exp} опыта.")

        while self.exp >= self.exp_to_next:
            self.level_up()

    def level_up(self):
        """Повышение уровня"""
        self.level += 1
        self.exp -= self.exp_to_next
        self.exp_to_next = int(self.exp_to_next * 1.5)  # Рост требуемого опыта

        # Увеличиваем базовые характеристики
        self.max_health += 50
        self.health = self.max_health
        self.attack += 10
        self.armor += 2
        self.mana = self.max_mana

        print(f"\n🎉 {self.name} достиг {self.level} уровня!")
        print(f"Характеристики улучшены: +50 ❤️, +10 💥, +2 🛡️")

        # Проверяем, есть ли скилл на этом уровне
        if str(self.level) in self.skills_db:
            for skill_data in self.skills_db[str(self.level)]:
                self.skills.append(skill_data.copy())
                print(f"✨ Вы изучили: {skill_data['name']} — {skill_data['desc']}")
    def add_exp(self, amount):
        self.exp += amount
        print(f"Получено {amount} опыта. Всего: {self.exp}.")

        while self.exp >= self.exp_to_next:
            self.level_up()

    def unlock_skill(self, name, description):
        """Разблокировка нового скилла"""
        self.skills.append({"name": name, "desc": description})
        print(f"✨ Разблокирован скилл: {name} — {description}")

    def show_skills(self):
        """Показывает доступные скиллы"""
        if not self.skills:
            print("❌ Нет изученных скиллов.")
            return False
        print("\n📚 Ваши скиллы:")
        for i, skill in enumerate(self.skills, 1):
            print(f"{i}. {skill['name']} — {skill['desc']}")
        return True

    def calculate_damage(self, is_magic=False, skill=None):
        """Рассчитывает физический или магический урон с критами"""
        """Рассчитывает урон с учётом скиллов и критов"""
        if skill:
            if skill == "Молния" and self.mana >= 30:
                self.mana -= 30
                base = 80 + self.spell_power * 0.5
                return int(base)
            elif skill == "Судный день" and self.mana >= 50:
                self.mana -= 50
                base = 150 + self.spell_power * 0.8
                return int(base)
            elif skill == "Божественный гнев":
                return 999  # Условный "мгновенный урон"
            else:
                print("❗ Недостаточно маны или скилл недоступен.")
                return 0

        if is_magic:
            if self.mana < 20:
                print("❗ Недостаточно маны!")
                return 0
            self.mana -= 20
            base_damage = self.spell_power
            crit = random.random() < self.crit_chance
            damage = base_damage * 1.5 if crit else base_damage
            if crit:
                print("🔥 Магический критический удар!")
            return int(damage)


        # Физическая атака
        crit = random.random() < self.crit_chance
        damage = self.attack * 2 if crit else self.attack
        if crit:
            print("💥 Критический удар!")
        return damage

    def use_health_potion(self):
        if self.inventory["health_potion"] > 0:
            heal = 150
            self.health = min(self.max_health, self.health + heal)
            self.inventory["health_potion"] -= 1
            print(f"🧪 Выпили зелье здоровья! Восстановлено {heal} ед. здоровья. Осталось: {self.inventory['health_potion']}")
        else:
            print("❗ Нет зелий здоровья!")

    def use_mana_potion(self):
        if self.inventory["mana_potion"] > 0:
            mana_restore = 60
            self.mana = min(100, self.mana + mana_restore)
            self.inventory["mana_potion"] -= 1
            print(f"🧪 Выпили зелье маны! Восстановлено {mana_restore} маны. Осталось: {self.inventory['mana_potion']}")
        else:
            print("❗ Нет зелий маны!")

    def restore_mana(self):
        self.mana = self.max_mana
        print("🌀 Мана восстановлена.")

    def show_inventory(self):
        print(f"\n🎒 Инвентарь:")
        print(f"   Зелья здоровья: {self.inventory['health_potion']}")
        print(f"   Зелья маны: {self.inventory['mana_potion']}")

    def __str__(self):
        return (f"{self.name} [{self.class_name}] "
                f"(Ур. {self.level}) — Здоровье: {self.health}, Атака: {self.attack}, "
                f"Броня: {self.armor}, Золото: {self.gold}, Опыт: {self.exp}")