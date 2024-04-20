# src/entities/enemy.py
import math

class Enemy:
    def __init__(self, x, y, size=100, speed=2, max_health=100, attack_damage=0.1, attack_range=50):
        self.initial_x = x
        self.initial_y = y
        self._x = x
        self._y = y
        self.size = size
        self.speed = speed
        self.max_health = max_health
        self.health = max_health
        self.alive = True
        self.attack_damage = attack_damage
        self.attack_range = attack_range

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def get_health_percentage(self):
        return (self.health / self.max_health) * 100

    def update(self, player):
        if not self.alive:
            return

        # Constants
        CHASE_DISTANCE = 500

        # Calculate distance to the player
        distance_to_player = math.sqrt((self.x - player._x) ** 2 + (self.y - player._y) ** 2)

        # If the player is within a certain distance, chase
        if distance_to_player < CHASE_DISTANCE:
            dx = player._x - self.x
            dy = player._y - self.y
            direction = math.atan2(dy, dx)

            # Move towards the player
            self.x += self.speed * math.cos(direction)
            self.y += self.speed * math.sin(direction)

    def attack_player(self, player):
        # Calculate distance to the player
        distance_to_player = math.sqrt((self.x - player._x) ** 2 + (self.y - player._y) ** 2)

        # Check if the player is within attack range
        if distance_to_player < self.attack_range:
            # Perform the attack on the player
            player.take_damage(self.attack_damage)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        self.alive = False
