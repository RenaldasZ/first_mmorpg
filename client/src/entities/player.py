# src/entities/player.py
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
        animation_list = []
        animation_steps = [7, 6] # number of frames for each animation (idle, walk)
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img_list.append(self.sprite_sheet.get_image(x, y, 100, 100, 1, (0, 0, 0)))
            animation_list.append(temp_img_list)
        return animation_list

    def update_animation(self):
        # Define the cooldown time
        ANIMATION_COOLDOWN = 100  # milliseconds

        # Get the current time
        current_time = pygame.time.get_ticks()

        # Check if it's time to update the animation
        if current_time - self.update_time > ANIMATION_COOLDOWN:
            # Update the update_time to the current time
            self.update_time = current_time

            # Move to the next frame
            self.frame_index += 1

            # Check if we've reached the end of the animation
            if self.frame_index >= len(self.animation_list[self.action]):
                # If so, reset the frame index to loop the animation
                self.frame_index = 0

        # Update the current image to the current frame
        self.image = self.animation_list[self.action][self.frame_index]
        print(f"action {self.action} frame_index {self.frame_index}")
            
    def update_action(self, new_action):
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
        # Remove specified item from the inventory
        if item in self.inventory.items:
            self.inventory.items.remove(item)

    def take_damage(self, damage):
        # Reduce player's health when taking damage
        self.health -= damage
        self.health = max(0, self.health)

    def heal(self, amount):
        # Increase player's health when healing
        self.health += amount
        self.health = min(MAX_PLAYER_HEALTH, self.health)
            
    def attack(self, enemy):
        # Calculate distance to the enemy
        distance_to_enemy = math.sqrt((self._x - enemy._x) ** 2 + (self._y - enemy._y) ** 2)
        
        # Check if the enemy is within attack range
        if distance_to_enemy < self.attack_range:
            enemy.take_damage(self.attack_damage)
