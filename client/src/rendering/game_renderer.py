# src/rendering/game_renderer.py
import pygame
from src.rendering.map_renderer import render_map
from datetime import datetime, timedelta
from src.entities.npc import NPC

WHITE = (255, 255, 255)

class GameRenderer:
    def __init__(self, game, viewport_factor=4):
        self.game = game
        self.time_factor = 6
        self.viewport_factor = viewport_factor
        self.last_update = datetime.now()
        self.enemy_image = pygame.image.load("assets/enemy/dog.png").convert_alpha()
        self.question_mark_image = pygame.image.load("assets/question_mark.png").convert_alpha()
        self.item_icons = {
            "Stick": pygame.image.load("assets/items/stick.png").convert_alpha(),
            "Empty vial": pygame.image.load("assets/items/empty_vial.png").convert_alpha(),
            "Vial of Water": pygame.image.load("assets/items/vial_of_water.png").convert_alpha(),
            "Axe Head": pygame.image.load("assets/items/axe_head.png").convert_alpha(),
            "Cutting Axe": pygame.image.load("assets/items/cutting_axe.png").convert_alpha(),
            "Gold Coin": pygame.image.load("assets/items/gold_coin.png").convert_alpha(),
        }
        self.inventory_slot_size = 50
        self.inventory_margin = 10
        self.inventory_font = pygame.font.Font(None, 20)

    def render(self):
        self.game.screen.fill(WHITE)
        render_map(self.game, viewport_factor=self.viewport_factor)
        self.render_players()
        self.render_enemies()
        self.render_time()
        self.game.player_renderer.render_player_coords()
        self.game.player_renderer.render_player_health()
        self.render_inventory()
        self.render_enemy_health()
        self.handle_mouse_right_click()
        self.handle_quests()
        self.render_npc_question_mark()
        self.game.interaction_manager.check_interaction()
        self.render_kill_count()

    def render_npc_question_mark(self):
        player = self.game.player
        screen_size = self.game.screen_size

        # For the first NPC
        npc1_x, npc1_y = self.game.NPC_POSITIONS[NPC.TILE_NPC_1]
        if not self.game.quest_handler.axe_head_returned or not self.game.quest_handler.stick_returned:
            screen_x = npc1_x - player._x + screen_size[0] // 2
            screen_y = npc1_y - player._y + screen_size[1] // 2 - self.question_mark_image.get_height()
            self.game.screen.blit(self.question_mark_image, (screen_x, screen_y))

        # For the second NPC
        npc2_x, npc2_y = self.game.NPC_POSITIONS[NPC.TILE_NPC_2]
        if self.game.quest_handler.axe_head_returned and self.game.quest_handler.stick_returned:
            screen_x = npc2_x - player._x + screen_size[0] // 2
            screen_y = npc2_y - player._y + screen_size[1] // 2 - self.question_mark_image.get_height()
            self.game.screen.blit(self.question_mark_image, (screen_x, screen_y))

    def handle_mouse_right_click(self):
        if pygame.mouse.get_pressed()[2]:
            mouse_pos = pygame.mouse.get_pos()
            self.handle_mouse_hover(mouse_pos)

    def handle_mouse_hover(self, mouse_pos):
        # Convert mouse position to map coordinates
        map_pos = self.game.screen_to_map(mouse_pos)
        # Determine the object ID under the mouse cursor
        object_id = self.get_object_id_at(map_pos)
        # Display the object ID next to the mouse cursor
        self.render_object_id(object_id, mouse_pos)

    def get_object_id_at(self, map_pos):
        # Calculate the tile or object ID at the given map position
        chunk_x = int(map_pos[0] // self.game.CHUNK_SIZE)
        chunk_y = int(map_pos[1] // self.game.CHUNK_SIZE)
        if 0 <= chunk_x < len(self.game.map_tiles[0]) and 0 <= chunk_y < len(self.game.map_tiles):
            return self.game.map_tiles[chunk_y][chunk_x]
        return None

    def render_object_id(self, object_id, mouse_pos):
        if object_id is not None:
            object_id_text = f"Object ID: {object_id}"
            text_surface = self.game.font.render(object_id_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.topleft = mouse_pos
            self.game.screen.blit(text_surface, text_rect)

    def render_kill_count(self):
        enemy_kill_count = self.game.player.enemy_kill_count 
        kill_count_text = f"Enemies killed: {enemy_kill_count}"
        text_surface = self.game.font.render(kill_count_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=(500, 500))
        self.game.screen.blit(text_surface, text_rect)

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

    def render_players(self):
        player_manager = self.game.player_manager
        for player in player_manager.players:
            player_size = player._size
            player_render_x = self.game.screen_size[0] // 2 - player_size // 2
            player_render_y = self.game.screen_size[1] // 2 - player_size // 2
            self.game.screen.blit(player.image, (player_render_x, player_render_y))

    def render_inventory(self):
        player_inventory = self.game.player.inventory
        inventory_rect = pygame.Rect(
            self.inventory_margin, 
            self.game.screen_size[1] - self.inventory_margin - self.inventory_slot_size,
            (self.inventory_slot_size + self.inventory_margin) * len(player_inventory.items) + self.inventory_margin,
            self.inventory_slot_size + self.inventory_margin * 2
        )
        pygame.draw.rect(self.game.screen, (0, 0, 0), inventory_rect, 2)

        slot_x = self.inventory_margin * 2
        slot_y = self.game.screen_size[1] - self.inventory_margin - self.inventory_slot_size + self.inventory_margin

        for item_name in player_inventory.items:
            item_icon = self.item_icons.get(item_name)
            if item_icon:
                # Resize the image to fit the inventory slot size
                resized_icon = pygame.transform.scale(item_icon, (self.inventory_slot_size, self.inventory_slot_size))
                item_rect = pygame.Rect(slot_x, slot_y, self.inventory_slot_size, self.inventory_slot_size)
                self.game.screen.blit(resized_icon, item_rect)

            # Render item name
            item_name_text = self.inventory_font.render(item_name, True, (255, 255, 255))
            item_name_rect = item_name_text.get_rect(
                center=(slot_x + self.inventory_slot_size // 2, slot_y + self.inventory_slot_size + self.inventory_margin)
            )
            self.game.screen.blit(item_name_text, item_name_rect)

            slot_x += self.inventory_slot_size + self.inventory_margin

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
