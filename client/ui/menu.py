import pygame
from ui.button import Button

class Menu:
    """
    Represents a menu screen in a Pygame application.

    Args:
        screen (pygame.Surface): The Pygame surface to render the menu on.
    """

    def __init__(self, screen):
        """
        Initializes the Menu object.

        Args:
            screen (pygame.Surface): The Pygame surface to render the menu on.
        """
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
        self.background_image = pygame.image.load("assets/mountain.png").convert()

        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
    
    def handle_events(self):
        """
        Handles events such as mouse clicks and window close events.

        Returns:
            str or None: The choice made by the user ('play game', 'exit', or 'quit') or None if no choice was made.
        """
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                choice = self.handle_button_click(event.pos)
                if choice:
                    return choice
            elif event.type == pygame.QUIT:
                return "quit"
    
    def handle_button_click(self, pos):
        """
        Handles button clicks.

        Args:
            pos (tuple): The position of the mouse click.

        Returns:
            str or None: The choice made by the user ('play game', 'exit') or None if no button was clicked.
        """
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                return button.text.lower()

    def render(self):
        """
        Renders the menu on the screen.
        """
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.title_text, self.title_rect)
        for button in self.buttons:
            button.render(self.screen)
