import pygame
from ui.button import Button

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font(None, 60)
        self.button_font = pygame.font.Font(None, 40)
        self.buttons = [
            Button("Play Game", self.width // 2, self.height // 2 - 50),
            Button("Exit", self.width // 2, self.height // 2 + 100)
        ]
        self.title_text = self.font.render("Welcome to Maras", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(self.width // 2, self.height // 4))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                choice = self.handle_button_click(event.pos)
                if choice:
                    return choice
            elif event.type == pygame.QUIT:
                return "quit"
    
    def handle_button_click(self, pos):
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                return button.text.lower()

    def render(self):
        self.screen.fill((64, 64, 64))  # dark gray
        self.screen.blit(self.title_text, self.title_rect)
        for button in self.buttons:
            button.render(self.screen)
