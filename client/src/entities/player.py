import pygame
from src.utils.stack import Stack
import math

DEFAULT_PLAYER_SIZE = 100
INITIAL_PLAYER_POSITION = (10000 / 2, 10000 / 2)
MAX_PLAYER_HEALTH = 100

class Player:
    def __init__(self, sprite_sheet, size=DEFAULT_PLAYER_SIZE, attack_damage=1, attack_range=100, enemy_kill_count=0):
        self._size = size
        self._x, self._y = INITIAL_PLAYER_POSITION
        self.rect = pygame.Rect(self._x, self._y, size, size)
        self.inventory = Stack()
        self.health = MAX_PLAYER_HEALTH
        self.attack_damage = attack_damage
        self.attack_range = attack_range
        self.enemy_kill_count = enemy_kill_count
        
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_animation()
        self.frame_index = 0
        self.action = 0 # 0: idle, 1: walk
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()

    def load_animation(self):
        """
        Loads the animation frames from the sprite sheet.
        """
        try:
            FRAME_WIDTH = 100
            FRAME_HEIGHT = 100
            SCALE = 1

            # Number of frames for each animation (idle, walk)
            animation_steps = [7, 6]

            # Create the animation list using list comprehensions
            animation_list = [
                [self.sprite_sheet.get_image(x, y, FRAME_WIDTH, FRAME_HEIGHT, SCALE) for x in range(steps)]
                for y, steps in enumerate(animation_steps)
            ]
            return animation_list
        except Exception as e:
            print(f"Error loading animations: {e}")
            return []

    def update_animation(self):
        """
        Updates the current frame of the animation based on the cooldown time.
        """
        ANIMATION_COOLDOWN = 100  # milliseconds
        current_time = pygame.time.get_ticks()

        if current_time - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = current_time
            self.frame_index = (self.frame_index + 1) % len(self.animation_list[self.action])
            self.image = self.animation_list[self.action][self.frame_index]
            print(f"action {self.action} frame_index {self.frame_index}")

    def update_action(self, new_action):
        """
        Updates the current action of the player.
        """
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    @property
    def position(self):
        return self._x, self._y

    @position.setter
    def position(self, new_position):
        self._x, self._y = new_position
        self.rect.topleft = new_position

    def add_to_inventory(self, item):
        self.inventory.push(item)

    def remove_from_inventory(self):
        return self.inventory.pop()

    def remove_item_from_inventory(self, item):
        if item in self.inventory.items:
            self.inventory.items.remove(item)

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def heal(self, amount):
        self.health = min(MAX_PLAYER_HEALTH, self.health + amount)
            
    def attack(self, enemy):
        """
        Attacks an enemy if within range.
        """
        if self._is_enemy_within_range(enemy):
            enemy.take_damage(self.attack_damage)

    def _is_enemy_within_range(self, enemy):
        """
        Helper function to check if the enemy is within attack range.
        """
        distance_to_enemy = math.hypot(self._x - enemy._x, self._y - enemy._y)
        return distance_to_enemy < self.attack_range
