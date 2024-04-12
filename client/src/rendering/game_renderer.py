# src/rendering/game_renderer.py
import pygame
from src.rendering.map_renderer import render_map
from datetime import datetime, timedelta

WHITE = (255, 255, 255)

class GameRenderer:
    def __init__(self, game):
        self.game = game
        self.time_factor = 6
        self.last_update = datetime.now()
        self.enemy_image = pygame.image.load("assets/enemy/dog.png").convert_alpha()
        self.viewport_factor = 1

    def render(self):
        self.game.screen.fill(WHITE)
        render_map(self.game)
        self.render_players()
        self.render_inventory()
        self.render_time()
        self.game.render_player_coords()
        self.game.render_player_health()
        self.render_enemies()
        self.render_enemy_health()
        self.game.check_interaction()
        self.handle_quests()

    def render_enemies(self):
        player = self.game.player
        screen_size = self.game.screen_size
        viewport_width = screen_size[0] * self.viewport_factor
        viewport_height = screen_size[1] * self.viewport_factor
        viewport_rect = pygame.Rect(player._x - viewport_width // 2, player._y - viewport_height // 2,
                                    viewport_width, viewport_height)

        for enemy in self.game.enemies:
            if enemy.alive:
                enemy_rect = pygame.Rect(enemy.x - enemy.size // 2, enemy.y - enemy.size // 2,
                                          enemy.size, enemy.size)
                if enemy_rect.colliderect(viewport_rect):
                    enemy_screen_pos = (
                        enemy.x - player._x + screen_size[0] // 2,
                        enemy.y - player._y + screen_size[1] // 2
                    )
                    self.game.screen.blit(self.enemy_image, enemy_screen_pos)

        pygame.display.flip()

    def render_players(self):
        screen = self.game.screen
        player_manager = self.game.player_manager
        for player in player_manager.players:
            player_size = player._size
            player_render_x = self.game.screen_size[0] // 2 - player_size // 2
            player_render_y = self.game.screen_size[1] // 2 - player_size // 2
            pygame.draw.rect(screen, (0, 0, 0), (player_render_x, player_render_y, player_size, player_size))

    def render_inventory(self):
        player_inventory = self.game.player.inventory
        inventory_text = "Inventory: " + ", ".join(player_inventory.items)
        text_surface = self.game.font.render(inventory_text, True, WHITE)
        text_rect = text_surface.get_rect(bottomleft=(20, self.game.screen_size[1] - 20))
        self.game.screen.blit(text_surface, text_rect)

    def render_time(self):
        current_time = self.calculate_time().strftime("%H:%M:%S")
        text_surface = self.game.font.render(current_time, True, WHITE)
        text_rect = text_surface.get_rect(topleft=(100, 100))
        self.game.screen.blit(text_surface, text_rect)

    def render_enemy_health(self):
        for enemy in self.game.enemies:
            if enemy.alive:
                enemy_screen_pos = (
                    enemy.x - self.game.player._x + self.game.screen_size[0] // 2,
                    enemy.y - self.game.player._y + self.game.screen_size[1] // 2
                )
                health_bar_x = enemy_screen_pos[0]
                health_bar_y = enemy_screen_pos[1] - 10
                health_ratio = enemy.get_health_percentage() / 100
                health_bar_width = int(self.game.player._size * health_ratio)
                health_bar_rect = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, 5)
                pygame.draw.rect(self.game.screen, (255, 0, 0), health_bar_rect)

    def calculate_time(self):
        time_difference = datetime.now() - self.last_update
        adjusted_time_difference = timedelta(seconds=time_difference.total_seconds() * self.time_factor)
        adjusted_time = self.last_update + adjusted_time_difference
        return adjusted_time

    def set_time_factor(self, factor):
        self.time_factor = factor

    def update_last_update_time(self):
        self.last_update = datetime.now()

    def handle_quests(self):
        if self.game.quest_handler.quest_active:
            self.game.quest_handler.handle_axe_pickup()

        if self.game.quest_handler.healing_quest_active and not self.game.quest_handler.quest_active:
            self.game.quest_handler.handle_vial_pickup()
