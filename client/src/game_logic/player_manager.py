# src/game_logic/player_manager.py
import pygame
from src.entities.player import MAX_PLAYER_HEALTH

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

MAP_WIDTH = 10000
MAP_HEIGHT = 10000
PLAYER_SPEED = 6
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
EXIT_BUTTON_OFFSET = 10

class PlayerManager:
    def __init__(self, game):
        self.game = game
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def update(self):
        if self.game.target_pos:
            self.move_player_to_target()

    def move_player_to_target(self):
        move_vector = pygame.math.Vector2(self.game.target_pos[0] - self.game.player.position[0], self.game.target_pos[1] - self.game.player.position[1])
        move_distance = move_vector.length()

        if move_distance > 0:
            move_vector.normalize_ip()
            move_vector *= min(move_distance, PLAYER_SPEED)
            new_pos = pygame.math.Vector2(self.game.player.position[0], self.game.player.position[1]) + move_vector

            if not self.game.collides_with_barrier(new_pos) and 0 <= new_pos.x <= MAP_WIDTH and 0 <= new_pos.y <= MAP_HEIGHT:
                self.game.player.position = (new_pos.x, new_pos.y)
        else:
            self.game.player.position = self.game.target_pos
            self.game.target_pos = None

    def render_player_coords(self):
        text_offset = EXIT_BUTTON_OFFSET
        player_coords_text = f"Player Coords: ({self.game.player._x}, {self.game.player._y})"
        chunk_coords_text = f"Chunk Coords: ({self.game.get_player_chunk()})"

        for i, text in enumerate([player_coords_text, chunk_coords_text]):
            text_surface = self.game.font.render(text, True, WHITE)
            self.game.screen.blit(text_surface, (text_offset, 10 + (i * 30)))

        self.render_exit_button()

    def render_player_health(self):
        player_health = self.game.player.health
        max_health = MAX_PLAYER_HEALTH
        health_bar_x = (self.game.screen_size[0] - HEALTH_BAR_WIDTH) // 2
        health_bar_y = self.game.screen_size[1] - EXIT_BUTTON_OFFSET * 2
        health_ratio = player_health / max_health
        health_bar_fill_width = int(health_ratio * HEALTH_BAR_WIDTH)
        health_bar_rect = pygame.Rect(health_bar_x, health_bar_y, health_bar_fill_width, HEALTH_BAR_HEIGHT)
        pygame.draw.rect(self.game.screen, (0, 255, 0), health_bar_rect)

    def render_exit_button(self):
        exit_text_surface = self.game.font.render("Exit Game", True, BLACK)
        exit_text_rect = exit_text_surface.get_rect()
        exit_text_rect.topleft = (self.game.screen_size[0] - exit_text_rect.width - EXIT_BUTTON_OFFSET, EXIT_BUTTON_OFFSET)
        exit_button_rect = exit_text_rect.inflate(EXIT_BUTTON_OFFSET, EXIT_BUTTON_OFFSET)
        pygame.draw.rect(self.game.screen, RED, exit_button_rect)
        self.game.screen.blit(exit_text_surface, exit_text_rect)

    def get_player_chunk(self):
        return self.game.player._x // self.game.CHUNK_SIZE, self.game.player._y // self.game.CHUNK_SIZE
