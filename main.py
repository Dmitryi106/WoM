from Player.Enemy import Enemy
from Player.Player import Player
import time

player_game = Player("DangerMaster")
enemy_game = Enemy("Мурлок")
while player_game.health > 0 and enemy_game.health > 0:
    player_game.health = player_game.health - enemy_game.attacks()
    enemy_game.health = enemy_game.health - player_game.attacks()
    print(f"Здоровье {player_game.name}: {player_game.health}")
    print(f"Здоровье {enemy_game.name}: {enemy_game.health}")
    time.sleep(0.5)

