# src/entities/skill.py

class Skill:
    """
    Represents a skill that a player can use in the game.
    """
    
    def __init__(self, name, icon, cooldown, damage):
        """
        Initialize the Skill instance.

        Args:
            name (str): The name of the skill.
            icon: The icon representing the skill.
            cooldown (float): The cooldown time between uses of the skill in seconds.
            damage (int): The amount of damage the skill deals.
        """
        self.name = name
        self.icon = icon
        self.cooldown = cooldown
        self.damage = damage
        self.last_used = 0

    def use(self, current_time):
        """
        Use the skill if the cooldown period has passed.

        Args:
            current_time (float): The current time in seconds.

        Returns:
            bool: True if the skill was successfully used, False otherwise.
        """
        if current_time - self.last_used >= self.cooldown:
            self.last_used = current_time
            return True
        return False
