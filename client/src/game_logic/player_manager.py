# src/game_logic/player_manager.py
import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

MAP_WIDTH = 10000
MAP_HEIGHT = 10000
PLAYER_SPEED = 5

class PlayerManager:
    def __init__(self, game):
        self.game = game
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def update(self):
        if self.game.target_pos:
            self.move_player_to_target()
        self.game.player.update_animation()

    def move_player_to_target(self):
        move_vector = pygame.math.Vector2(self.game.target_pos[0] - self.game.player.position[0], self.game.target_pos[1] - self.game.player.position[1])
        move_distance = move_vector.length()

        if move_distance > 0:
            move_vector.normalize_ip()
            move_vector *= min(move_distance, PLAYER_SPEED)
            new_pos = pygame.math.Vector2(self.game.player.position[0], self.game.player.position[1]) + move_vector

            if not self.game.collides_with_barrier(new_pos) and 0 <= new_pos.x <= MAP_WIDTH and 0 <= new_pos.y <= MAP_HEIGHT:
                self.game.player.position = (new_pos.x, new_pos.y)
                self.game.player.update_action(1)  # Walking animation
            else:
                self.game.player.update_action(0)  # Idle animation
        else:
            self.game.player.position = self.game.target_pos
            self.game.target_pos = None
            self.game.player.update_action(0)  # Idle animation
