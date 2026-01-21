import pygame
import sys
import random
from WoM.Player.Player import Player
from WoM.Player.Enemy import Enemy
from WoM.Battle.Battle import Battle

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("World of Meele — RPG")
clock = pygame.time.Clock()
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (50, 205, 50)
BLUE = (30, 144, 255)
GRAY = (169, 169, 169)
GOLD = (255, 215, 0)

# Шрифты
font_large = pygame.font.SysFont("Arial", 36, bold=True)
font_medium = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 22)

# Загрузка изображений
ASSETS_PATH = "GameTron/WoM/assets"
try:
    player_img = pygame.image.load(f"{ASSETS_PATH}/player.png")
    player_img = pygame.transform.scale(player_img, (150, 150))
    print("✅ player.png загружен")
except Exception as e:
    print(f"❌ Не удалось загрузить player.png: {e}")
    player_img = None

try:
    enemy_img = pygame.image.load(f"{ASSETS_PATH}/enemy.png")
    enemy_img = pygame.transform.scale(enemy_img, (150, 150))
    print("✅ enemy.png загружен")
except Exception as e:
    print(f"❌ Не удалось загрузить enemy.png: {e}")
    enemy_img = None

# Иконки (если есть)
icons = {}
try:
    icons["health"] = pygame.image.load(f"{ASSETS_PATH}/icons/health.png")
    icons["mana"] = pygame.image.load(f"{ASSETS_PATH}/icons/mana.png")
    icons["exp"] = pygame.image.load(f"{ASSETS_PATH}/icons/exp.png")
    icons["gold"] = pygame.image.load(f"{ASSETS_PATH}/icons/gold.png")
    for k in icons:
        icons[k] = pygame.transform.scale(icons[k], (24, 24))
    print("✅ Все иконки загружены")
except Exception as e:
    print(f"❌ Не удалось загрузить иконки: {e}")
    icons = {}
try:
    icons["health"] = pygame.image.load(f"{ASSETS_PATH}/icons/health.png")
    icons["mana"] = pygame.image.load(f"{ASSETS_PATH}/icons/mana.png")
    icons["exp"] = pygame.image.load(f"{ASSETS_PATH}/icons/exp.png")
    icons["gold"] = pygame.image.load(f"{ASSETS_PATH}/icons/gold.png")
    for k in icons:
        icons[k] = pygame.transform.scale(icons[k], (24, 24))
except:
    icons = {}  # если нет — используем текст

# Глобальные переменные
player = None
enemy = None
battle = None
game_state = "menu"  # menu, battle, game_over
buttons = []
return_to_menu_timer = None  # Таймер для возврата в меню
RETURN_DELAY = 2000  # 2 секунды


# === Класс кнопки ===
class Button:
    def __init__(self, x, y, w, h, text, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.action = action
        self.hovered = False

    def draw(self, screen):
        color = (100, 150, 255) if self.hovered else (135, 206, 250)
        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=12)
        text_surface = font_small.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False


# === Отрисовка полосы здоровья ===
def draw_health_bar(x, y, current, max_val, label=""):
    bar_width = 200
    bar_height = 20
    fill = (current / max_val) * bar_width
    fill = max(fill, 0)

    # Фон
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (x, y, fill, bar_height))
    pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height), 2)

    # Текст
    label_text = font_small.render(f"{label}: {int(current)}/{max_val}", True, WHITE)
    screen.blit(label_text, (x, y - 25))

# === Отрисовка статуса игрока (слева, рядом с HP) ===
def draw_player_status():
    """Отображает уровень, золото, ману и опыт рядом с полосой здоровья"""
    x = 50  # Рядом с health bar
    y = 140  # Под HP
    spacing = 30

    # Фоновая панель
    pygame.draw.rect(screen, (25, 25, 50), (x - 10, y - 10, 280, 130), border_radius=12)
    pygame.draw.rect(screen, GOLD, (x - 10, y - 10, 280, 130), 2, border_radius=12)

    # Уровень
    level_text = font_small.render(f"Уровень: {player.level}", True, WHITE)
    screen.blit(level_text, (x, y))

    # Золото
    if "gold" in icons:
        screen.blit(icons["gold"], (x, y + spacing))
        gold_text = font_small.render(f" {player.gold}", True, GOLD)
        screen.blit(gold_text, (x + 30, y + spacing))
    else:
        gold_text = font_small.render(f"Золото: {player.gold}", True, GOLD)
        screen.blit(gold_text, (x, y + spacing))

    # Мана
    if "mana" in icons:
        screen.blit(icons["mana"], (x, y + spacing * 2))
        mana_text = font_small.render(f" {player.mana}/{player.max_mana}", True, (100, 200, 255))
        screen.blit(mana_text, (x + 30, y + spacing * 2))
    else:
        mana_text = font_small.render(f"Мана: {player.mana}/{player.max_mana}", True, (100, 200, 255))
        screen.blit(mana_text, (x, y + spacing * 2))

    # Опыт
    if "exp" in icons:
        screen.blit(icons["exp"], (x, y + spacing * 3))
        exp_text = font_small.render(f" {player.exp}/{player.exp_to_next}", True, (100, 255, 100))
        screen.blit(exp_text, (x + 30, y + spacing * 3))
    else:
        exp_text = font_small.render(f"Опыт: {player.exp}/{player.exp_to_next}", True, (100, 255, 100))
        screen.blit(exp_text, (x, y + spacing * 3))

        # Полоса опыта
    exp_bar_width = 180
    exp_fill = (player.exp / player.exp_to_next) * exp_bar_width
    exp_fill = max(exp_fill, 0)
    pygame.draw.rect(screen, (50, 50, 50), (x, y + spacing * 3 + 25, exp_bar_width, 10))
    pygame.draw.rect(screen, (100, 255, 100), (x, y + spacing * 3 + 25, exp_fill, 10))
    pygame.draw.rect(screen, WHITE, (x, y + spacing * 3 + 25, exp_bar_width, 10), 1)

# === Экран меню ===
def draw_menu():
    screen.fill((20, 20, 40))
    title = font_large.render("World of Meele", True, GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

    subtitle = font_medium.render("Нажмите ПРОБЕЛ, чтобы начать", True, WHITE)
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 200))

    global buttons
    buttons = [
        Button(WIDTH // 2 - 150, 300, 300, 50, "⚔️ В бой", "battle"),
        Button(WIDTH // 2 - 150, 370, 300, 50, "🛒 Магазин", "shop"),
    ]

    for btn in buttons:
        btn.draw(screen)

    if player:
        draw_player_status()

# === Отрисовка лога ===
LOG_AREA_HEIGHT = 120
LOG_LINES = 4

# === Отрисовка лога ===
def draw_log():
    pygame.draw.rect(screen, (30, 30, 50), (0, HEIGHT - LOG_AREA_HEIGHT, WIDTH, LOG_AREA_HEIGHT))
    pygame.draw.line(screen, WHITE, (0, HEIGHT - LOG_AREA_HEIGHT), (WIDTH, HEIGHT - LOG_AREA_HEIGHT), 2)
    if battle:
        messages = battle.log_messages[-LOG_LINES:]  # последние 4 строки
        for i, msg in enumerate(messages):
            text = font_small.render(msg, True, WHITE)
            screen.blit(text, (10, HEIGHT - LOG_AREA_HEIGHT + 10 + i * 25))


# === Создание кнопок боя — по центру снизу ===
def create_battle_buttons():
    global buttons
    button_width = 180
    button_height = 50
    gap = 20
    total_width = 4 * button_width + 3 * gap  # 4 кнопки + 3 промежутка
    start_x = (WIDTH - total_width) // 2  # центрируем по ширине
    y = HEIGHT - 150  # над логом

    buttons = [
        Button(start_x, y, button_width, button_height, "Атаковать", "attack"),
        Button(start_x + button_width + gap, y, button_width, button_height, "Предмет", "item"),
        Button(start_x + 2*(button_width + gap), y, button_width, button_height, "Сбежать", "escape"),
        Button(start_x + 3*(button_width + gap), y, button_width, button_height, "Скилл", "skill") if player.skills else None,
    ]
    buttons = [b for b in buttons if b]  # удаляем None

# === Состояние выбора скилла ===
def create_skill_select_buttons():
    global buttons
    skills = battle.use_skill()  # получаем список скиллов
    if not skills:
        return

    buttons = []
    for i, skill in enumerate(skills):
        mana_cost = skill.get("mana_cost", 0)
        btn = Button(
            WIDTH // 2 - 150,
            200 + i * 70,
            300,
            50,
            f"{skill['name']} ({mana_cost} маны)",
            f"skill_{i}"
        )
        buttons.append(btn)

# === Отрисовка выбора скилла ===
def draw_skill_select():
    screen.fill((20, 20, 40))
    title = font_large.render("Выберите скилл", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

    for btn in buttons:
        btn.draw(screen)


# === Отрисовка магазина ===
def draw_shop():
    screen.fill((10, 20, 40))
    title = font_large.render("Магазин", True, GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

    subtitle = font_medium.render("Здесь можно купить зелья", True, WHITE)
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 160))

    # Кнопки магазина
    global buttons
    buttons = [
        Button(WIDTH // 2 - 150, 250, 300, 50, "🧪 Зелье здоровья (10 золота)", "buy_health"),
        Button(WIDTH // 2 - 150, 320, 300, 50, "💧 Зелье маны (15 золота)", "buy_mana"),
        Button(WIDTH // 2 - 150, 390, 300, 50, "⬅️ Назад", "back"),
    ]

    for btn in buttons:
        btn.draw(screen)

# === Запуск боя ===
def start_battle():
    global battle, enemy, game_state
    enemy = Enemy(str(random.randint(1, 10)))
    battle = Battle(player, enemy)
    game_state = "battle"
    create_battle_buttons()


# === Главный цикл ===
def main():
    global player, game_state, return_to_menu_timer, buttons

    player = Player("1", "Герой")
    player.add_exp(0)

    running = True
    while running:
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == "menu":
                for btn in buttons:
                    btn.check_hover(pos)
                    if btn.is_clicked(pos, event):
                        if btn.action == "battle":
                            start_battle()
                        elif btn.action == "shop":
                            game_state = "shop"

            elif game_state == "battle":
                for btn in buttons:
                    btn.check_hover(pos)
                    if btn.is_clicked(pos, event):
                        handle_battle_action(btn.action)

            elif game_state == "skill_select":
                for btn in buttons:
                    btn.check_hover(pos)
                    if btn.is_clicked(pos, event):
                        if btn.action.startswith("skill_"):
                            skill_idx = int(btn.action.split("_")[1])
                            battle.execute_skill(skill_idx)
                            game_state = "battle"
                            create_battle_buttons()  # возвращаем основные кнопки
                            battle.enemy_turn()  # ход врага после использования

            elif game_state == "shop":
                for btn in buttons:
                    btn.check_hover(pos)
                    if btn.is_clicked(pos, event):
                        if btn.action == "buy_health":
                            if player.gold >= 10:
                                player.gold -= 10
                                player.inventory["health_potion"] += 1
                                print("🛒 Куплено зелье здоровья!")
                        elif btn.action == "buy_mana":
                            if player.gold >= 15:
                                player.gold -= 15
                                player.inventory["mana_potion"] += 1
                                print("🛒 Куплено зелье маны!")
                        elif btn.action == "back":
                            game_state = "menu"
# Обновление состояния
        # Обновление состояния
        if battle and battle.is_finished():
            if return_to_menu_timer is None:
                return_to_menu_timer = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - return_to_menu_timer > RETURN_DELAY:
                # Меняем состояние ТОЛЬКО если мы всё ещё в бою или в меню
                if game_state in ["battle", "menu"]:
                    game_state = "menu"
                battle.log_messages.append("Бой окончен. Возврат в меню...")
                return_to_menu_timer = None
        else:
            # Если бой неактивен, но мы НЕ в магазине — сбрасываем таймер
            if game_state != "battle":
                return_to_menu_timer = None

        # Отрисовка
        if game_state == "menu":
            draw_menu()
        elif game_state == "battle":
            draw_battle()
        elif game_state == "skill_select":
            draw_skill_select()
        elif game_state == "shop":
            draw_shop()

        pygame.display.flip()
        clock.tick(FPS)


# === Обработка действий в бою ===
def handle_battle_action(action):
    global battle
    if not battle or battle.is_finished():
        return

    if action == "attack":
        battle.player_attack()
        if battle.is_finished():
            return
        battle.enemy_turn()  # Ход врага
    elif action == "item":
        battle.use_item()
        if battle.is_finished():
            return
        battle.enemy_turn()
    elif action == "escape":
        battle.attempt_escape()
    elif action == "skill":
        # ✅ Переход в режим выбора скилла
        global game_state
        game_state = "skill_select"
        create_skill_select_buttons()  # создаём кнопки скиллов

# === Отрисовка боя ===
def draw_battle():
    screen.fill((10, 10, 30))

    # Названия
    vs_text = font_large.render(f"{player.name} vs {enemy.name}", True, WHITE)
    screen.blit(vs_text, (WIDTH // 2 - vs_text.get_width() // 2, 20))

    # Спрайт игрока
    if player_img:
        screen.blit(player_img, (50, 250))
    else:
        pygame.draw.rect(screen, (100, 100, 255), (50, 250, 150, 150))  # заглушка

    # Спрайт врага
    if enemy_img:
        screen.blit(enemy_img, (WIDTH - 200, 250))
    else:
        pygame.draw.rect(screen, (255, 100, 100), (WIDTH - 200, 250, 150, 150))  # заглушка

    # Полосы здоровья
    draw_health_bar(50, 100, player.health, player.max_health, f"{player.name}")
    draw_health_bar(WIDTH - 250, 100, enemy.health, enemy.max_health, f"{enemy.name}")

    # Статус игрока — рядом с его HP
    draw_player_status()

    # Кнопки действий
    for btn in buttons:
        btn.draw(screen)

    draw_log()



if __name__ == "__main__":
    main()

