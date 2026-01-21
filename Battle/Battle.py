from WoM.Player.Player import Player
from WoM.Player.Enemy import Enemy
import random


class Battle:
    """Боевая система — только логика, без ввода/вывода в консоль"""

    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.log_messages = []
        self.is_battle_active = True

    def log(self, message):
        """Добавляет сообщение в лог (отображается в GUI)"""
        self.log_messages.append(message)

    def player_attack(self):
        """Игрок атакует врага"""
        if not self.is_battle_active:
            return

        damage = self.player.calculate_damage(is_magic=False)
        self.enemy.health -= damage
        self.log(f"💥 {self.player.name} наносит {damage} урона!")

        if not self.enemy.is_alive():
            self.log(f"💀 {self.enemy.name} повержен!")
            self.grant_victory()

    def use_item(self):
        """Использование предмета"""
        if not self.is_battle_active:
            return

        if self.player.inventory["health_potion"] > 0:
            self.player.use_health_potion()
            self.log("🧪 Использовано зелье здоровья!")
        else:
            self.log("❌ Нет зелий здоровья!")

    def use_skill(self):
        """Возвращает список скиллов — для GUI"""
        if not self.player.skills:
            self.log("❌ Нет доступных скиллов.")
            return None
        return self.player.skills  # возвращаем список для отображения

    def execute_skill(self, skill_index):
        """Выполняет скилл по индексу"""
        if skill_index < 0 or skill_index >= len(self.player.skills):
            return

        skill = self.player.skills[skill_index]
        mana_cost = skill.get("mana_cost", 0)

        if self.player.mana < mana_cost:
            self.log("❗ Недостаточно маны!")
            return

        self.player.mana -= mana_cost

        if skill["type"] == "damage":
            damage = skill["base_damage"] + int(self.player.spell_power * skill["scaling"])
            self.enemy.health -= damage
            self.log(f"⚡ {skill['name']}! Нанесено {damage} урона!")
        elif skill["type"] == "effect" and skill["effect"] == "kill_weak":
            if self.enemy.health < skill["threshold"]:
                self.enemy.health = 0
                self.log("🔥 Враг уничтожен!")
            else:
                self.log("❌ Враг слишком силён.")

        if not self.enemy.is_alive():
            self.grant_victory()

    def attempt_escape(self):
        """Попытка побега"""
        if random.random() < 0.5:
            self.log(f"🏃‍♂️ {self.player.name} сбегает!")
            self.end_battle(victory=False)
            return True
        else:
            self.log("❌ Побег не удался!")
            return False

    def enemy_turn(self):
        """Ход врага"""
        if not self.is_battle_active or not self.player.is_alive():
            return

        reduced_damage = max(1, self.enemy.attack - self.player.armor)
        self.player.health -= reduced_damage
        self.log(f"👹 {self.enemy.name} атакует! Нанесено {reduced_damage} урона.")

        if not self.player.is_alive():
            self.log("💀 Вы погибли!")
            self.end_battle(victory=False)

    def grant_victory(self):
        """Награда за победу"""
        gold_reward = random.randint(10, 30)
        self.player.gold += gold_reward
        self.player.add_exp(self.enemy.reward_exp)
        self.log(f"🏆 Победа! Получено {gold_reward} золота и {self.enemy.reward_exp} опыта.")
        self.end_battle(victory=True)

    def end_battle(self, victory):
        """Завершение боя"""
        self.is_battle_active = False

    def is_finished(self):
        """Проверка, завершён ли бой"""
        return not self.is_battle_active

    def use_skill(self):
        """Возвращает список скиллов для отображения"""
        if not self.player.skills:
            self.log("❌ Нет доступных скиллов.")
            return None
        return self.player.skills  # возвращаем список

    def execute_skill(self, skill_index):
        """Выполняет скилл по индексу"""
        if skill_index < 0 or skill_index >= len(self.player.skills):
            return

        skill = self.player.skills[skill_index]
        mana_cost = skill.get("mana_cost", 0)

        if self.player.mana < mana_cost:
            self.log("❗ Недостаточно маны!")
            return

        self.player.mana -= mana_cost

        if skill["type"] == "damage":
            damage = skill["base_damage"] + int(self.player.spell_power * skill["scaling"])
            self.enemy.health -= damage
            self.log(f"⚡ {skill['name']}! Нанесено {damage} урона!")
        elif skill["type"] == "effect" and skill["effect"] == "kill_weak":
            if self.enemy.health < skill["threshold"]:
                self.enemy.health = 0
                self.log("🔥 Враг уничтожен!")
            else:
                self.log("❌ Враг слишком силён.")

        if not self.enemy.is_alive():
            self.grant_victory()