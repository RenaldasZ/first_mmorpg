# src/game_logic/game.py
import pygame
from src.entities import Player, Enemy, NPC, Skill
from src.systems import InputHandler
from src.game_logic import PlayerManager, QuestHandler, SpawnManager, TransitionManager, InteractionManager
from src.rendering import GameRenderer, PlayerRenderer, SkillInventoryRenderer, TILE_WELL, TILE_TREE
from src.utils import ItemHandler, collides_with_barrier, SpriteSheet

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

        self.sprite_sheet = SpriteSheet("assets/player/player_spritesheet.png")
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

        self.transition_manager.load_map('maps/map.json')
        self.spawn_manager.spawn_enemies()

        self.skill_inventory_renderer = SkillInventoryRenderer(self.player, self.screen, self.font)

        attack_1_icon = pygame.image.load('assets/player/skill1.png')
        attack_2_icon = pygame.image.load('assets/player/skill2.png')

        attack_1 = Skill('attack_1', attack_1_icon, cooldown=1000, damage=10)
        attack_2 = Skill('attack_2', attack_2_icon, cooldown=2000, damage=50)

        self.player.add_skill(attack_1)
        self.player.add_skill(attack_2)

    def handle_events(self):
        """Handle game events such as player inputs, NPC interactions, and transitions."""
        self.input_handler.handle_events()
        self.check_transition_area_collision()
        self.handle_npc_interaction(NPC.TILE_NPC_1)
        self.handle_npc_interaction(NPC.TILE_NPC_2)
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

    def enemy_within_range(self, player_x, player_y, attack_range):
        """
        Check if there is an enemy within the player's attack range.

        Args:
            player_x (float): The x-coordinate of the player.
            player_y (float): The y-coordinate of the player.
            attack_range (float): The attack range of the player.

        Returns:
            Enemy: The nearest enemy within range if found, else None.
        """
        for enemy in self.enemies:
            if enemy.alive and self.player._is_enemy_within_range(enemy):
                return enemy
        return None

    def spawn_enemy(self, x, y):
        """
        Spawn a new enemy at the specified coordinates.

        Args:
            x (float): The x-coordinate to spawn the enemy.
            y (float): The y-coordinate to spawn the enemy.
        """
        new_enemy = Enemy(x, y, self)
        self.enemies.append(new_enemy)

    def handle_mouse_click(self, mouse_pos):
        """
        Handle mouse click events, including skill selection and target position setting.

        Args:
            mouse_pos (tuple): The position of the mouse click (x, y).
        """
        skill_rects = self.skill_inventory_renderer.get_skill_rects()
        for i, rect in enumerate(skill_rects):
            if rect.collidepoint(mouse_pos):
                self.player.select_skill(i)
                return
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
            else:
                enemy.update(self.player)

    def render(self):
        """Render the game state on the screen."""
        self.renderer.render()
        self.player_renderer.render_player_coords()
        self.player_renderer.render_player_health()
        self.skill_inventory_renderer.render()
        self.renderer.render_kill_count()

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
