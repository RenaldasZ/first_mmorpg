# src/entities/player.py
import pygame
from src.utils import Stack
import math

DEFAULT_PLAYER_SIZE = 100
INITIAL_PLAYER_POSITION = (10000 / 2, 10000 / 2)
MAX_PLAYER_HEALTH = 100

class Player:
    """
    Represents the player in the game, handling position, health, inventory, and animations.
    """
    
    def __init__(self, sprite_sheet, size=DEFAULT_PLAYER_SIZE, attack_damage=0, attack_range=100, enemy_kill_count=0):
        """
        Initialize the Player instance.

        Args:
            sprite_sheet (SpriteSheet): The sprite sheet containing player animations.
            size (int): The size of the player sprite.
            attack_damage (int): The damage dealt by the player in an attack.
            attack_range (int): The range within which the player can attack enemies.
            enemy_kill_count (int): The initial count of enemies killed by the player.
        """
        self._size = size
        self._x, self._y = INITIAL_PLAYER_POSITION
        self.rect = pygame.Rect(self._x, self._y, size, size)
        self.inventory = Stack()
        self.health = MAX_PLAYER_HEALTH
        self.attack_damage = attack_damage
        self.attack_range = attack_range
        self.enemy_kill_count = enemy_kill_count
        
        self.sprite_sheet = sprite_sheet
        self.animation_list = {}
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: walk, 2: jump, 3: attack_1, 4: attack_2, 5: get_hit, 6: die
        self.load_animation(self.action)
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.current_attack = None

        self.skills = []
        self.selected_skill_index = 0

        self.action_temporary = False  # Flag to indicate if the action is temporary

        self.death_time = None
        self.respawn_delay = 1000  # 1 seconds delay for death animation
        self.is_dead = False

        # Attributes for leveling
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 60
        self.max_health = MAX_PLAYER_HEALTH

    def load_animation(self, action):
        """
        Load the animation frames from the sprite sheet for a specific action.

        Args:
            action (int): The action to load animations for.
        """
        try:
            FRAME_WIDTH = 100
            FRAME_HEIGHT = 100
            SCALE = 1

            # Number of frames for each animation (idle, walk, jump, attack_1, attack_2, get_hit, die)
            animation_steps = [7, 6, 0, 4, 4, 4, 10]

            if action not in self.animation_list:
                self.animation_list[action] = [
                    self.sprite_sheet.get_image(x, action, FRAME_WIDTH, FRAME_HEIGHT, SCALE)
                    for x in range(animation_steps[action])
                ]
        except Exception as e:
            print(f"Error loading animations: {e}")

    def update_animation(self):
        """
        Update the current frame of the animation based on the cooldown time.
        """
        current_time = pygame.time.get_ticks()
    
        ANIMATION_COOLDOWN = 100

        if current_time - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = current_time
            self.frame_index += 1

            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action_temporary:
                    self.update_action(0)  # Return to idle
                else:
                    self.frame_index = 0  # Loop the animation

            self.image = self.animation_list[self.action][self.frame_index]
            # print(f"Updated animation frame: {self.frame_index} for action: {self.action}")

    def update_action(self, new_action, temporary=False):
        """
        Update the current action of the player.

        Args:
            new_action (int): The new action to be set (0: idle, 1: walk, 2: jump, 3: attack_1, 4: attack_2, 5: get_hit, 6: die).
            temporary (bool): Flag indicating if the action is temporary and should return to idle afterward.
        """
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            self.load_animation(new_action)
            self.action_temporary = temporary
            # print(f"Action updated to: {self.action}, temporary: {self.action_temporary}")

    @property
    def position(self):
        """
        Get the current position of the player.

        Returns:
            tuple: The current position (x, y).
        """
        return self._x, self._y

    @position.setter
    def position(self, new_position):
        """
        Set the new position of the player.

        Args:
            new_position (tuple): The new position (x, y).
        """
        self._x, self._y = new_position
        self.rect.topleft = new_position

    def add_to_inventory(self, item):
        """
        Add an item to the player's inventory.

        Args:
            item: The item to be added to the inventory.
        """
        self.inventory.push(item)

    def remove_from_inventory(self):
        """
        Remove the top item from the player's inventory.

        Returns:
            The removed item.
        """
        return self.inventory.pop()

    def remove_item_from_inventory(self, item):
        """
        Remove a specific item from the player's inventory.

        Args:
            item: The item to be removed from the inventory.
        """
        if item in self.inventory.items:
            self.inventory.items.remove(item)

    def take_damage(self, damage):
        """
        Reduce the player's health by a specified damage amount and update action to get_hit.

        Args:
            damage (int): The amount of damage to be taken.
        """
        self.health = max(0, self.health - damage)
        self.update_action(5, temporary=True)
        if self.health == 0 and not self.is_dead:
            self.update_action(6)  # Die action does not revert to idle
            self.death_time = pygame.time.get_ticks()
            self.is_dead = True

    def update(self):
        """
        Update player state, including animations and checking for respawn.
        """
        if self.is_dead and pygame.time.get_ticks() - self.death_time >= self.respawn_delay:
            self.respawn()
        else:
            self.update_animation()  # Update animation if not dead or waiting to respawn

    def respawn(self):
        """
        Respawn the player by resetting the position and health.
        """
        self.position = INITIAL_PLAYER_POSITION
        self.health = MAX_PLAYER_HEALTH
        self.update_action(0)
        self.is_dead = False
        print("Player has respawned at the initial position with full health.")

    def heal(self, amount):
        """
        Heal the player by a specified amount.

        Args:
            amount (int): The amount of health to be restored.
        """
        self.health = min(self.max_health, self.health + amount)

    def add_skill(self, skill):
        """
        Add a skill to the player's skill list.

        Args:
            skill (Skill): The skill to be added.
        """
        self.skills.append(skill)

    def select_skill(self, index):
        """
        Select a skill from the skill list.

        Args:
            index (int): The index of the skill to be selected.
        """
        if 0 <= index < len(self.skills):
            self.selected_skill_index = index

    def use_selected_skill(self, enemy):
        """
        Use the selected skill on an enemy.

        Args:
            enemy (Enemy): The enemy to use the skill on.
        """
        if self.skills:
            skill = self.skills[self.selected_skill_index]
            if skill.use(pygame.time.get_ticks()):
                enemy.take_damage(skill.damage)
                print(f"Used skill: {skill.name} on enemy at position ({enemy._x}, {enemy._y})")
                # Set the appropriate action for the skill
                if self.selected_skill_index == 0:
                    self.update_action(3, temporary=True)  # attack_1 is a temporary action
                elif self.selected_skill_index == 1:
                    self.update_action(4, temporary=True)  # attack_2 is a temporary action

    def _is_enemy_within_range(self, enemy):
        """
        Check if the enemy is within the player's attack range.

        Args:
            enemy: The enemy to be checked.

        Returns:
            bool: True if the enemy is within range, False otherwise.
        """
        distance_to_enemy = math.hypot(self._x - enemy._x, self._y - enemy._y)
        return distance_to_enemy < self.attack_range

    def increase_kill_count(self, experience_points):
        """Increase the kill count and add experience when an enemy is killed."""
        self.enemy_kill_count += 1
        self.add_experience(experience_points)

    def add_experience(self, amount):
        """
        Add experience points to the player and handle leveling up.

        Args:
            amount (int): The amount of experience points to be added.
        """
        self.experience += amount
        while self.experience >= self.experience_to_next_level:
            self.level_up()

    def total_attack_damage(self):
        """
        Calculate the total attack damage considering the selected skill's damage.
        """
        if self.skills:
            selected_skill = self.skills[self.selected_skill_index]
            return self.attack_damage + selected_skill.damage
        return self.attack_damage

    def level_up(self):
        """Handle the player leveling up."""
        self.experience -= self.experience_to_next_level
        self.level += 1
        self.experience_to_next_level = int(self.experience_to_next_level * 1.5)  # Example: Increase required XP by 50%
        self.attack_damage += 5  # Example: Increase attack damage

        self.max_health += 20    # Example: Increase max health
        self.health = self.max_health  # Heal player to full health upon leveling up
        print(f"Leveled up! New level: {self.level}, New max health: {self.max_health}, New attack damage: {self.attack_damage}")