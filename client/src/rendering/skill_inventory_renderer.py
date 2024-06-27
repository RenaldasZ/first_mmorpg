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
