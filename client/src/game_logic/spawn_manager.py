# src/game_logic/spawn_manager.py
from src.entities.enemy import Enemy

class SpawnManager:
    def __init__(self, game):
        self.game = game

    def spawn_enemies(self):
        enemy_positions = [
            (5337, 6520), (4480, 6248), (3769, 5822), (3546, 5101), (3252, 4235),
            (3797, 3286), (4628, 2841), (6078, 2799), (6820, 3296), (7188, 3953),
            (7578, 4897), (7200, 5746), (6773, 6305)
        ]
        self.game.enemies = [Enemy(x, y, self.game) for x, y in enemy_positions]

    def spawn_enemy(self, x, y):
        new_enemy = Enemy(x, y, self.game)
        self.game.enemies.append(new_enemy)
        self.game.enemy = new_enemy
        print(self.game.enemy.x, self.game.enemy.y, self.game.enemy.alive)

    def spawn_enemies_second_map(self):
        enemy_positions = [
            (7000, 7000), (7200, 7200), (7400, 7400)
        ]
        self.game.enemies = [Enemy(x, y, self.game) for x, y in enemy_positions]