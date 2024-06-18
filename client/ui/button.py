# ui/button.py
import pygame

class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.font = pygame.font.Font(None, 40)
        self.width = 200
        self.height = 60
        self.color = (100, 100, 100)  # Dark gray color
        self.hover_color = (150, 150, 150)  # Lighter gray color
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
    
    def render(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
