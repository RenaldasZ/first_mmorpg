# src/utils/sprite_sheet.py
import pygame

class SpriteSheet:
    def __init__(self):
        self.sheet = pygame.image.load("assets/player/player_spritesheet.png").convert_alpha()
    
    def get_image(self, frame, row, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * width, row * height, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image