# src/game_logic/game.py
import pygame
import math
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.npc import NPC
from src.systems.input_handler import InputHandler
from src.rendering.game_renderer import GameRenderer
from src.rendering.map_renderer import TILE_WELL, TILE_TREE
from src.game_logic.player_manager import PlayerManager
from src.game_logic.quest_handler import QuestHandler
from src.game_logic.spawn_manager import SpawnManager
from src.game_logic.transition_manager import TransitionManager
from src.game_logic.interaction_manager import InteractionManager
from src.rendering.player_renderer import PlayerRenderer
from src.utils.item_handler import ItemHandler
from src.utils.barrier import collides_with_barrier
from src.utils.sprite_sheet import SpriteSheet

class Game:
    """Main game class responsible for initializing and managing the game state, including player, NPCs, enemies, and game events."""
    
    TILE_WELL = TILE_WELL
    TILE_TREE = TILE_TREE

    # NPC positions (x, y) in the map
    NPC_POSITIONS = {
        NPC.TILE_NPC_1: (5280, 4850),
        NPC.TILE_NPC_2: (5680, 3850),
    }

    def __init__(self, screen_size, screen):
        """
        Initialize the Game instance.

        Args:
            screen_size (tuple): The size of the game screen (width, height).
            screen (pygame.Surface): The surface to render the game on.
        """
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
        self.item_handler = ItemHandler(self.player)
        self.quest_handler = QuestHandler(self.player, self.screen_size, self.screen, self.item_handler)
        self.spawn_manager = SpawnManager(self)
        self.transition_manager = TransitionManager(self)
        self.interaction_manager = InteractionManager(self)
        self.player_renderer = PlayerRenderer(self)
        self.npc = NPC(self.quest_handler)
        self.enemies = []
        self.enemy = None

        # Use transition_manager to load the initial map
        self.transition_manager.load_map('maps/map.json')
        self.spawn_manager.spawn_enemies()

    def handle_events(self):
        """Handle game events such as player inputs, NPC interactions, and transitions."""
        self.input_handler.handle_events()
        self.check_transition_area_collision()
        self.handle_npc_interaction(NPC.TILE_NPC_1)
        self.handle_npc_interaction(NPC.TILE_NPC_2)
        self.handle_player_attack()
        self.interaction_manager.check_interaction()

    def check_transition_area_collision(self):
        """Check if the player collides with the transition area to trigger a map transition."""
        if not self.transitioning and self.player.rect.colliderect(self.transition_area):
            self.transition_manager.transition_to_second_map()

    def handle_npc_interaction(self, tile_id):
        """
        Handle interactions with NPCs.

        Args:
            tile_id (int): The tile ID of the NPC.
        """
        if self.map_tiles[int(self.player._y) // self.CHUNK_SIZE][int(self.player._x) // self.CHUNK_SIZE] == tile_id:
            if tile_id == NPC.TILE_NPC_1:
                self.npc.handle_interaction(self.player, tile_id)
            elif tile_id == NPC.TILE_NPC_2:
                self.npc.handle_interaction(self.player, tile_id)

    def handle_player_attack(self):
        """Handle player's attacks on enemies and update enemy states accordingly."""
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
        """
        Respawn a dead enemy at its initial position.

        Args:
            enemy (Enemy): The enemy to respawn.
        """
        index = self.enemies.index(enemy)
        self.enemies[index] = Enemy(enemy.initial_x, enemy.initial_y)

    def spawn_enemy(self, x, y):
        """Spawns a new enemy at the specified coordinates."""
        new_enemy = Enemy(x, y)
        self.enemies.append(new_enemy)

    def handle_mouse_click(self, mouse_pos):
        """
        Handle mouse click events and set the target position for the player.

        Args:
            mouse_pos (tuple): The position of the mouse click (x, y).
        """
        self.target_pos = self.screen_to_map(mouse_pos)

    def screen_to_map(self, screen_pos):
        """
        Convert screen coordinates to map coordinates.

        Args:
            screen_pos (tuple): The position on the screen (x, y).

        Returns:
            tuple: Corresponding map coordinates (x, y).
        """
        return (
            screen_pos[0] + self.player._x - self.screen_size[0] // 2,
            screen_pos[1] + self.player._y - self.screen_size[1] // 2
        )

    def update(self):
        """Update the game state, including player and enemy updates."""
        self.player_manager.update()
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(self.player)
                enemy.attack_player(self.player)

    def render(self):
        """Render the game state on the screen."""
        self.renderer.render()
        self.player_renderer.render_player_coords()
        self.player_renderer.render_player_health()

    def get_player_chunk(self):
        """
        Get the current chunk coordinates of the player.

        Returns:
            tuple: The chunk coordinates (chunk_x, chunk_y).
        """
        return self.player_manager.get_player_chunk()

    def collides_with_barrier(self, pos):
        """
        Check if a position collides with any barriers on the map.

        Args:
            pos (tuple): The position to check (x, y).

        Returns:
            bool: True if the position collides with a barrier, False otherwise.
        """
        return collides_with_barrier(pos, self.map_tiles, self.CHUNK_SIZE)
