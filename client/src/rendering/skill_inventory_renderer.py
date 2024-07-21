# src/ui/skill_inventory_renderer.py
import pygame

class SkillInventoryRenderer:
    def __init__(self, player, screen, font):
        self.player = player
        self.screen = screen
        self.font = font

    def render(self):
        x, y = 200, 200
        skill_size = 50
        
        # Render player stats
        level_text = self.font.render(f"Level: {self.player.level} | XP: {self.player.experience}/{self.player.experience_to_next_level}", True, (255, 255, 255))
        health_text = self.font.render(f"Health: {self.player.health}", True, (255, 255, 255))
        attack_damage_text = self.font.render(f"Attack Damage: {self.player.total_attack_damage()}", True, (255, 255, 255))
        attack_range_text = self.font.render(f"Attack Range: {self.player.attack_range}", True, (255, 255, 255))
        self.screen.blit(level_text, (x, y - 80))
        self.screen.blit(health_text, (x, y - 60))
        self.screen.blit(attack_damage_text, (x, y - 40))
        self.screen.blit(attack_range_text, (x, y - 20))

        for i, skill in enumerate(self.player.skills):
            rect = pygame.Rect(x + i * (skill_size + 10), y, skill_size, skill_size)
            pygame.draw.rect(self.screen, (255, 255, 255), rect)
            self.screen.blit(skill.icon, rect.topleft)
            if i == self.player.selected_skill_index:
                pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)

    def get_skill_rects(self):
        x, y = 200, 200
        skill_size = 50
        return [pygame.Rect(x + i * (skill_size + 10), y, skill_size, skill_size) for i in range(len(self.player.skills))]
