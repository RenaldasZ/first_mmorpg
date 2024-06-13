# src/game_logic/game.py
import pygame
import json
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.systems.input_handler import InputHandler
from src.rendering.game_renderer import GameRenderer
from src.rendering.map_renderer import TILE_NPC1, TILE_NPC2, TILE_WELL, TILE_TREE
from src.game_logic.player_manager import PlayerManager
from src.game_logic.quest_handler import QuestHandler
from src.utils.item_handler import ItemHandler
from src.utils.barrier import collides_with_barrier
from src.utils.sprite_sheet import SpriteSheet
import math

class Game:
    TILE_NPC_1 = TILE_NPC1
    TILE_NPC_2 = TILE_NPC2
    TILE_WELL = TILE_WELL
    TILE_TREE = TILE_TREE

    # NPC positions (x, y) in the map
    NPC_POSITIONS = {
        TILE_NPC_1: (5280, 4850),
        TILE_NPC_2: (5680, 3850),
    }

    def __init__(self, screen_size, screen):
        # Initialize game components
        self.screen_size = screen_size
        self.screen = screen
        self.running = True
        self.CHUNK_SIZE = 200
        self.font = pygame.font.Font(None, 24)
        self.target_pos = None
        self.transition_area = pygame.Rect(9800, 200, 200, 200)
        self.transitioning = False

        # Initialize and use the SpriteSheet class
        self.sprite_sheet = SpriteSheet()
        self.player = Player(self.sprite_sheet)

        self.player_manager = PlayerManager(self)
        self.player_manager.add_player(self.player)
        self.input_handler = InputHandler(self)
        self.renderer = GameRenderer(self)
        self.load_map('maps/map.json')
        self.item_handler = ItemHandler(self.player)
        self.quest_handler = QuestHandler(self.player, self.screen_size, self.screen, self.item_handler)
        self.enemies = []
        self.enemy = None
        self.spawn_enemies()

    def spawn_enemies(self):
        enemy_positions = [
            (5337, 6520), (4480, 6248), (3769, 5822), (3546, 5101), (3252, 4235),
            (3797, 3286), (4628, 2841), (6078, 2799), (6820, 3296), (7188, 3953),
            (7578, 4897), (7200, 5746), (6773, 6305)
        ]
        self.enemies = [Enemy(x, y) for x, y in enemy_positions]

    def spawn_enemy(self, x, y):
        new_enemy = Enemy(x, y)
        self.enemies.append(new_enemy)
        self.enemy = new_enemy
        print(self.enemy.x, self.enemy.y, self.enemy.alive)

    def spawn_enemies_second_map(self):
        enemy_positions = [
            (7000, 7000), (7200, 7200), (7400, 7400)
        ]
        self.enemies = [Enemy(x, y) for x, y in enemy_positions]

    def handle_events(self):
        self.input_handler.handle_events()
        self.check_transition_area_collision()
        self.handle_npc_interaction(self.TILE_NPC_1)
        self.handle_npc_interaction(self.TILE_NPC_2)
        self.handle_player_attack()
        self.check_interaction()

    def check_transition_area_collision(self):
        if not self.transitioning and self.player.rect.colliderect(self.transition_area):
            self.transition_to_second_map()

    def handle_npc_interaction(self, tile_id):
        if self.map_tiles[int(self.player._y) // self.CHUNK_SIZE][int(self.player._x) // self.CHUNK_SIZE] == tile_id:
            if tile_id == self.TILE_NPC_1:
                if not self.quest_handler.quest_active and not self.quest_handler.axe_head_returned:
                    self.quest_handler.start_quest()
                elif self.quest_handler.quest_active and not self.quest_handler.axe_head_returned:
                    self.quest_handler.return_axe_head()
                elif self.quest_handler.axe_head_returned and not self.quest_handler.stick_returned:
                    self.quest_handler.return_stick()
            elif tile_id == self.TILE_NPC_2:
                if not self.quest_handler.healing_quest_active and not self.quest_handler.empty_vial_returned:
                    self.quest_handler.healing_quest_start()
                elif self.quest_handler.healing_quest_active and not self.quest_handler.empty_vial_returned:
                    self.quest_handler.return_empty_vial()
                elif self.quest_handler.healing_quest_active and not self.quest_handler.filled_vial_of_water:
                    self.quest_handler.vial_of_water_quest()

    def handle_player_attack(self):
        # Check for collisions between player and enemies
        for enemy in self.enemies:
            if enemy.alive:
                distance_to_enemy = math.sqrt((self.player._x - enemy.x) ** 2 + (self.player._y - enemy.y) ** 2)
                if distance_to_enemy < self.player.attack_range:
                    enemy.take_damage(self.player.attack_damage)
                    if not enemy.alive:
                        self.player.enemy_kill_count += 1
                        print(self.player.enemy_kill_count)
                        self.respawn_enemy(enemy)

    def respawn_enemy(self, enemy):
        # Find the index of the dead enemy
        index = self.enemies.index(enemy)
        # Respawn the enemy at its initial position
        self.enemies[index] = Enemy(enemy.initial_x, enemy.initial_y)

    def check_interaction(self):
        # Get the player's position in terms of chunks
        player_x_chunk = int((self.player._x + self.player._size / 2) // self.CHUNK_SIZE)
        player_y_chunk = int((self.player._y + self.player._size / 2) // self.CHUNK_SIZE)

        # Define the range of chunks to check around the player
        chunk_range = range(player_x_chunk - 1, player_x_chunk + 1)
        chunk_range_y = range(player_y_chunk - 1, player_y_chunk + 1)

        # Iterate over the surrounding chunks to check for interactions
        for chunk_x in chunk_range:
            for chunk_y in chunk_range_y:
                # Ensure chunk indices are within bounds of the map
                if 0 <= chunk_x < len(self.map_tiles[0]) and 0 <= chunk_y < len(self.map_tiles):
                    # Handle well interaction
                    if self.map_tiles[chunk_y][chunk_x] == self.TILE_WELL:
                        self.handle_well_interaction()
                        return
                    # Handle tree interaction
                    elif self.map_tiles[chunk_y][chunk_x] == self.TILE_TREE:
                        self.handle_tree_interaction()
                        return

    def handle_well_interaction(self):
        self.player.heal(0.1)
        if "Empty vial" in self.player.inventory.items and self.quest_handler.empty_vial_returned:
            self.player.remove_item_from_inventory("Empty vial")
            self.player.add_to_inventory("Vial of Water")

    def handle_tree_interaction(self):
        if "Stick" not in self.player.inventory.items:
            self.player.add_to_inventory("Stick")
                        
    def transition_to_second_map(self):
        if not self.transitioning:
            self.load_map('maps/map2.json') 
            self.spawn_enemies_second_map()
            self.player.position = (9800, 9800)
            self.transitioning = True
            item = "Health Potion"
            self.player.add_to_inventory(item)

    def load_map(self, map_filename):
        try:
            with open(map_filename, 'r') as f:
                self.map_tiles = json.load(f)
        except FileNotFoundError:
            print(f"Error: Map file '{map_filename}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in map file '{map_filename}'.")

    def handle_mouse_click(self, mouse_pos):
        self.target_pos = self.screen_to_map(mouse_pos)

    def screen_to_map(self, screen_pos):
        return (
            screen_pos[0] + self.player._x - self.screen_size[0] // 2,
            screen_pos[1] + self.player._y - self.screen_size[1] // 2
        )

    def update(self):
        self.player_manager.update()
        # Update all enemies
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(self.player)
                enemy.attack_player(self.player)

    def render(self):
        self.renderer.render()
        self.render_player_coords()
        self.render_player_health()

    def render_player_coords(self):
        self.player_manager.render_player_coords()

    def render_player_health(self):
        self.player_manager.render_player_health()

    def get_player_chunk(self):
        return self.player_manager.get_player_chunk()

    def collides_with_barrier(self, pos):
        return collides_with_barrier(pos, self.map_tiles, self.CHUNK_SIZE)
