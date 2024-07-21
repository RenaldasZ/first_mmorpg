# src/game_logic/spawn_manager.py

from src.entities import Enemy

class SpawnManager:
    def __init__(self, game):
        self.game = game

    def spawn_enemies(self):
        enemy_positions = [
            (4300, 4300), (4480, 6248), (3769, 5822), (3546, 5101), (3252, 4235),
            (3797, 3286), (4628, 2841), (6078, 2799), (6820, 3296), (7188, 3953),
            (7578, 4897), (7200, 5746), (6773, 6305)
        ]
        levels = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3]  # Define levels for enemies
        self.game.enemies = [Enemy(x, y, self.game, level) for (x, y), level in zip(enemy_positions, levels)]

    def spawn_enemy(self, x, y, level=1):
        """
        Spawn a new enemy at the specified coordinates and level.

        Args:
            x (float): The x-coordinate to spawn the enemy.
            y (float): The y-coordinate to spawn the enemy.
            level (int): The level of the enemy to spawn.
        """
        new_enemy = Enemy(x, y, self.game, level=level)
        self.game.enemies.append(new_enemy)
        self.game.enemy = new_enemy
        print(self.game.enemy.x, self.game.enemy.y, self.game.enemy.alive)

    def spawn_enemies_second_map(self):
        enemy_positions = [
            (7000, 7000), (7200, 7200), (7400, 7400)
        ]
        levels = [6, 7, 8]  # Define levels for enemies in the second map
        self.game.enemies = [Enemy(x, y, self.game, level) for (x, y), level in zip(enemy_positions, levels)]
