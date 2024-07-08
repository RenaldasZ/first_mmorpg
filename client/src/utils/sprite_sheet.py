# src/utils/sprite_sheet.py
import pygame

class SpriteSheet:
    def __init__(self, file_path):
        self.sheet = pygame.image.load(file_path).convert_alpha()
    
    def get_image(self, frame, row, width, height, scale):
        # Create a new blank image with transparency
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        # Copy the sprite from the sheet onto the new image
        image.blit(self.sheet, (0, 0), (frame * width, row * height, width, height))
        # Scale the image
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))

        return image