# src/entities/enemy.py

import math
import random
import time

class Enemy:
    """
    Represents an enemy in the game, handling position, movement, health, and attacks.
    """

    CHASE_DISTANCE = 200  # Distance within which the enemy will chase the player
    MIN_COOLDOWN = 2.0    # Minimum cooldown time between attacks
    MAX_COOLDOWN = 7.0    # Maximum cooldown time between attacks
    MIN_RESPAWN_TIME = 5  # Minimum respawn time in seconds
    MAX_RESPAWN_TIME = 10 # Maximum respawn time in seconds

    def __init__(self, x, y, game, level=1, size=100, speed=2, max_health=100, attack_range=100):
        """
        Initialize the Enemy instance.

        Args:
            x (float): The initial x-coordinate of the enemy.
            y (float): The initial y-coordinate of the enemy.
            level (int): The level of the enemy.
            size (int): The size of the enemy sprite.
            speed (float): The movement speed of the enemy.
            max_health (int): The maximum health of the enemy.
            attack_range (float): The range within which the enemy can attack.
        """
        self.initial_x = x
        self.initial_y = y
        self._x = x
        self._y = y
        self.level = level
        self.size = size
        self.speed = speed
        self.max_health = max_health + (level - 1) * 20  # Increase health with level
        self.health = self.max_health
        self.alive = True
        self.attack_range = attack_range
        self.last_attack_time = 0
        self.attack_cooldown = self._random_cooldown()
        self.respawn_time = self._random_respawn_time()
        self.respawn_timer = 0
        self.game = game

    @property
    def x(self):
        """Get the current x-coordinate of the enemy."""
        return self._x

    @x.setter
    def x(self, value):
        """Set a new x-coordinate for the enemy."""
        self._x = value

    @property
    def y(self):
        """Get the current y-coordinate of the enemy."""
        return self._y

    @y.setter
    def y(self, value):
        """Set a new y-coordinate for the enemy."""
        self._y = value

    def get_health_percentage(self):
        """
        Get the current health as a percentage of the maximum health.

        Returns:
            float: Current health as a percentage of max health.
        """
        return (self.health / self.max_health) * 100

    def update(self, player):
        """
        Update the enemy's state, including movement towards the player if within chase distance.

        Args:
            player (Player): The player object to interact with.
        """
        if not self.alive:
            if time.time() >= self.respawn_timer:
                self.respawn()
            return

        distance_to_player = self._calculate_distance(player._x, player._y)

        if distance_to_player < self.CHASE_DISTANCE:
            self._move_towards(player._x, player._y)
            self.attack_player(player)

    def respawn(self):
        """Respawn the enemy at its initial position."""
        self._x = self.initial_x
        self._y = self.initial_y
        self.health = self.max_health
        self.alive = True
        self.respawn_time = self._random_respawn_time()

    def attack_player(self, player):
        """
        Attack the player if within attack range and the cooldown period has passed.

        Args:
            player (Player): The player object to attack.
        """
        current_time = time.time()
        if self._is_within_range(player._x, player._y, self.attack_range) and (current_time - self.last_attack_time) >= self.attack_cooldown:
            random_attack_damage = random.randint(1, 3) + (self.level - 1)  # Increase damage with level
            player.take_damage(random_attack_damage)
            self.last_attack_time = current_time
            self.attack_cooldown = self._random_cooldown()

    def take_damage(self, damage):
        """
        Reduce the enemy's health and destroy the enemy if health falls to zero or below.

        Args:
            damage (float): The amount of damage to be taken.
        """
        self.health -= damage
        if self.health <= 0:
            self.destroy()

    def get_experience_reward(self):
        """
        Calculate the experience points awarded to the player when this enemy is defeated.
        
        Returns:
            int: The experience points reward based on the enemy's level.
        """
        base_experience = 10  # Base experience points
        level_multiplier = 1.5  # Multiplier to increase experience based on enemy's level
        return int(base_experience + (self.level - 1) * level_multiplier)
    
    def destroy(self):
        """Mark the enemy as dead and start the respawn timer."""
        self.alive = False
        self.respawn_timer = time.time() + self.respawn_time
        # Notify the game to increment the player's kill count and add experience
        self.game.player.increase_kill_count(self.get_experience_reward())

    def _calculate_distance(self, target_x, target_y):
        """
        Calculate the distance to a target point.

        Args:
            target_x (float): The x-coordinate of the target.
            target_y (float): The y-coordinate of the target.

        Returns:
            float: The distance to the target point.
        """
        return math.sqrt((self.x - target_x) ** 2 + (self.y - target_y) ** 2)

    def _move_towards(self, target_x, target_y):
        """
        Move the enemy towards the target coordinates.

        Args:
            target_x (float): The x-coordinate of the target.
            target_y (float): The y-coordinate of the target.
        """
        dx = target_x - self.x
        dy = target_y - self.y
        direction = math.atan2(dy, dx)
        self.x += self.speed * math.cos(direction)
        self.y += self.speed * math.sin(direction)

    def _is_within_range(self, target_x, target_y, attack_range):
        """
        Check if a target is within a given range.

        Args:
            target_x (float): The x-coordinate of the target.
            target_y (float): The y-coordinate of the target.
            range (float): The range to check against.

        Returns:
            bool: True if the target is within range, False otherwise.
        """
        return self._calculate_distance(target_x, target_y) < attack_range

    def _random_cooldown(self):
        """
        Generate a random cooldown duration between attacks.

        Returns:
            float: A random cooldown duration in seconds.
        """
        return random.uniform(self.MIN_COOLDOWN, self.MAX_COOLDOWN)

    def _random_respawn_time(self):
        """
        Generate a random respawn time within the defined range.

        Returns:
            float: A random respawn time in seconds.
        """
        return random.uniform(self.MIN_RESPAWN_TIME, self.MAX_RESPAWN_TIME)
