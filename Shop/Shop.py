import os
import time
from WoM.Player.Player import Player


class Shop:
    """Класс, описывающий магазин для покупки зелий и предметов"""

    items = [
        {"name": "Зелье здоровья", "price": 30, "effect": "heal", "value": 150},
        {"name": "Зелье маны", "price": 25, "effect": "mana_restore", "value": 60},
        {"name": "Малое зелье опыта", "price": 50, "effect": "exp", "value": 50},
    ]

    @staticmethod
    def show_items():
        """Показывает товары магазина"""
        print("\n🛍️ Добро пожаловать в магазин!")
        print("Вот что у нас есть:\n")
        for i, item in enumerate(Shop.items, 1):
            print(f"{i}. {item['name']} — {item['price']} золота — {Shop.get_description(item)}")

    @staticmethod
    def get_description(item):
        """Возвращает описание предмета"""
        if item["effect"] == "heal":
            return f"Восстанавливает {item['value']} ❤️"
        elif item["effect"] == "mana_restore":
            return f"Восстанавливает {item['value']} 🌀"
        elif item["effect"] == "exp":
            return f"Даёт {item['value']} опыта"
        return ""

    @staticmethod
    def open(player: Player):
        """Открывает магазин для игрока"""
        while True:
            print(f"\n💰 Ваше золото: {player.gold}")
            Shop.show_items()
            print("0. Выйти из магазина")

            try:
                choice = input("\nВыберите товар: ").strip()
                if choice == "0":
                    print("Вы вышли из магазина.")
                    break

                idx = int(choice) - 1
                if idx < 0 or idx >= len(Shop.items):
                    print("❗ Неверный номер товара.")
                    time.sleep(1)
                    continue

                item = Shop.items[idx]
                if player.gold < item["price"]:
                    print("❗ У вас недостаточно золота!")
                    time.sleep(1)
                    continue

                # Покупка
                player.gold -= item["price"]
                Shop.give_item(player, item)
                print(f"✅ Вы купили: {item['name']}")

                # Спросим, хочет ли игрок купить ещё что-то
                cont = input("\nХотите купить что-то ещё? (да/нет): ").strip().lower()
                if cont not in ["да", "д", "yes", "y"]:
                    print("Вы вышли из магазина.")
                    break

            except ValueError:
                print("❗ Введите число.")
                time.sleep(1)
            except KeyboardInterrupt:
                print("\n\nВы вышли из магазина.")
                break

    @staticmethod
    def give_item(player: Player, item: dict):
        """Выдаёт купленный предмет игроку"""
        if item["effect"] == "heal":
            player.inventory["health_potion"] += 1
        elif item["effect"] == "mana_restore":
            player.inventory["mana_potion"] += 1
        elif item["effect"] == "exp":
            player.add_exp(item["value"])