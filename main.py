from Player.Enemy import Enemy
from Player.Player import Player

player_game = Player("DangerMaster")
enemy_game = Enemy("Мурлок")

print(player_game.health - enemy_game.attacks())

