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
        """Returns the current health as a percentage of the max health."""
        return (self.health / self.max_health) * 100

    def update(self, player):
        """Updates the enemy's state, including movement towards the player if within chase distance."""
        if not self.alive:
            return

        CHASE_DISTANCE = 500  # Distance within which the enemy will chase the player

        distance_to_player = self._calculate_distance(player._x, player._y)

        if distance_to_player < CHASE_DISTANCE:
            self._move_towards(player._x, player._y)

    def attack_player(self, player):
        """Attacks the player if within attack range."""
        if self._is_within_range(player._x, player._y, self.attack_range):
            player.take_damage(self.attack_damage)

    def take_damage(self, damage):
        """Reduces the enemy's health and destroys the enemy if health falls to zero or below."""
        self.health -= damage
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        """Marks the enemy as dead."""
        self.alive = False

    def _calculate_distance(self, target_x, target_y):
        """Calculates the distance to a target point."""
        return math.sqrt((self.x - target_x) ** 2 + (self.y - target_y) ** 2)

    def _move_towards(self, target_x, target_y):
        """Moves the enemy towards the target coordinates."""
        dx = target_x - self.x
        dy = target_y - self.y
        direction = math.atan2(dy, dx)
        self.x += self.speed * math.cos(direction)
        self.y += self.speed * math.sin(direction)

    def _is_within_range(self, target_x, target_y, range):
        """Checks if a target is within a given range."""
        return self._calculate_distance(target_x, target_y) < range
