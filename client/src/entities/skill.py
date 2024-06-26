# src/entities/skill.py

class Skill:
    def __init__(self, name, icon, cooldown, damage):
        self.name = name
        self.icon = icon
        self.cooldown = cooldown
        self.damage = damage
        self.last_used = 0

    def use(self, current_time):
        if current_time - self.last_used >= self.cooldown:
            self.last_used = current_time
            return True
        return False
