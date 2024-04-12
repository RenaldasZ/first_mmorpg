# src/game_logic/input_handler.py
import pygame
from ui.exit_button_renderer import is_exit_button_clicked

class InputHandler:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.handle_quit_event()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_event(event)

    def handle_quit_event(self):
        # Handle quit event by stopping the game loop
        self.game.running = False

    def handle_mouse_click(self, mouse_pos):
        # Handle mouse click event
        if is_exit_button_clicked(mouse_pos, self.game.font, self.game.screen_size):
            self.handle_quit_event()  # Exit button clicked
        else:
            self.game.handle_mouse_click(mouse_pos)

    def handle_keydown_event(self, event):
        # Handle key down event
        if event.key == pygame.K_e:
            self.handle_e_key_press()  # 'e' key pressed

    def handle_e_key_press(self):
        # Handle 'e' key press by spawning an enemy
        self.game.spawn_enemy(self.game.player._x, self.game.player._y)
