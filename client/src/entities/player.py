import pygame
from src.utils.stack import Stack
import math

DEFAULT_PLAYER_SIZE = 100
INITIAL_PLAYER_POSITION = (10000 / 2, 10000 / 2)
MAX_PLAYER_HEALTH = 100

class Player:
    def __init__(self, size=DEFAULT_PLAYER_SIZE, attack_damage=1, attack_range=100, enemy_kill_count=0):
        self._size = size
        self._x, self._y = INITIAL_PLAYER_POSITION
        self.rect = pygame.Rect(self._x, self._y, size, size)
        self.inventory = Stack()
        self.health = MAX_PLAYER_HEALTH
        self.attack_damage = attack_damage
        self.attack_range = attack_range
        self.enemy_kill_count = enemy_kill_count

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
