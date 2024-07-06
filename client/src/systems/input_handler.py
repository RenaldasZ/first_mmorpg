# src/systems/input_handler.py
import pygame
from ui.exit_button_renderer import is_exit_button_clicked

class InputHandler:
    def __init__(self, game):
        """
        Initialize the InputHandler with the game instance.

        Args:
            game: The game instance to handle input for.
        """
        self.game = game

    def handle_events(self):
        """
        Handle the various events in the game loop, such as quit, mouse clicks, and key presses.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.handle_quit_event()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_click(pygame.mouse.get_pos(), event.button)
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_event(event)

    def handle_quit_event(self):
        """
        Handle the quit event by stopping the game loop.
        """
        self.game.running = False

    def handle_mouse_click(self, mouse_pos, button):
        """
        Handle mouse click events.

        Args:
            mouse_pos: The position of the mouse click.
            button: The mouse button that was clicked.
        """
        if is_exit_button_clicked(mouse_pos, self.game.font, self.game.screen_size):
            self.handle_quit_event()
        elif button == 1:
            self.game.handle_mouse_click(mouse_pos)
        elif button == 3:
            enemy = self.game.enemy_within_range(self.game.player._x, self.game.player._y, self.game.player.attack_range)
            if enemy:
                self.game.player.use_selected_skill(enemy)

    def handle_keydown_event(self, event):
        """
        Handle key down events.

        Args:
            event: The key event.
        """
        if event.key == pygame.K_e:
            self.handle_e_key_press()
        elif event.key == pygame.K_1:
            self.game.player.select_skill(0)
        elif event.key == pygame.K_2:
            self.game.player.select_skill(1)

    def handle_e_key_press(self):
        """
        Handle the 'e' key press event to spawn an enemy at the player's location.
        """
        self.game.spawn_enemy(self.game.player._x, self.game.player._y)
