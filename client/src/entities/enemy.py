# src/entities/enemy.py
import math

class Enemy:
    """
    Represents an enemy in the game, handling position, movement, health, and attacks.
    """

    def __init__(self, x, y, size=100, speed=2, max_health=100, attack_damage=0.1, attack_range=50):
        """
        Initialize the Enemy instance.

        Args:
            x (float): The initial x-coordinate of the enemy.
            y (float): The initial y-coordinate of the enemy.
            size (int): The size of the enemy sprite.
            speed (float): The movement speed of the enemy.
            max_health (int): The maximum health of the enemy.
            attack_damage (float): The damage dealt by the enemy in an attack.
            attack_range (float): The range within which the enemy can attack.
        """
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
        """
        Get the current x-coordinate of the enemy.

        Returns:
            float: The current x-coordinate.
        """
        return self._x

    @x.setter
    def x(self, value):
        """
        Set a new x-coordinate for the enemy.

        Args:
            value (float): The new x-coordinate.
        """
        self._x = value

    @property
    def y(self):
        """
        Get the current y-coordinate of the enemy.

        Returns:
            float: The current y-coordinate.
        """
        return self._y

    @y.setter
    def y(self, value):
        """
        Set a new y-coordinate for the enemy.

        Args:
            value (float): The new y-coordinate.
        """
        self._y = value

    def get_health_percentage(self):
        """
        Get the current health as a percentage of the maximum health.

        Returns:
            float: The current health percentage.
        """
        return (self.health / self.max_health) * 100

    def update(self, player):
        """
        Update the enemy's state, including movement towards the player if within chase distance.

        Args:
            player (Player): The player object to interact with.
        """
        if not self.alive:
            return

        CHASE_DISTANCE = 500  # Distance within which the enemy will chase the player

        distance_to_player = self._calculate_distance(player._x, player._y)

        if distance_to_player < CHASE_DISTANCE:
            self._move_towards(player._x, player._y)

    def attack_player(self, player):
        """
        Attack the player if within attack range.

        Args:
            player (Player): The player object to attack.
        """
        if self._is_within_range(player._x, player._y, self.attack_range):
            player.take_damage(self.attack_damage)

    def take_damage(self, damage):
        """
        Reduce the enemy's health and destroy the enemy if health falls to zero or below.

        Args:
            damage (float): The amount of damage to be taken.
        """
        self.health -= damage
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        """
        Mark the enemy as dead.
        """
        self.alive = False

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

    def _is_within_range(self, target_x, target_y, range):
        """
        Check if a target is within a given range.

        Args:
            target_x (float): The x-coordinate of the target.
            target_y (float): The y-coordinate of the target.
            range (float): The range to check against.

        Returns:
            bool: True if the target is within range, False otherwise.
        """
        return self._calculate_distance(target_x, target_y) < range
