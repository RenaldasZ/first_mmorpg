# src/systems/input_handler.py

import pygame
from ui.exit_button_renderer import is_exit_button_clicked

class InputHandler:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.handle_quit_event()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_click(pygame.mouse.get_pos(), event.button)
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_event(event)

    def handle_quit_event(self):
        # Handle quit event by stopping the game loop
        self.game.running = False

    def handle_mouse_click(self, mouse_pos, button):
        if is_exit_button_clicked(mouse_pos, self.game.font, self.game.screen_size):
            self.handle_quit_event()  # Exit button clicked
        else:
            self.game.handle_mouse_click(mouse_pos)
        
        # Call the use_selected_skill method on right mouse button click
        if button == 3:  # Right mouse button is button 3
            enemy = self.game.enemy_within_range(self.game.player._x, self.game.player._y, self.game.player.attack_range)
            if enemy:
                self.game.player.use_selected_skill(enemy)

    def handle_keydown_event(self, event):
        if event.key == pygame.K_e:
            self.handle_e_key_press()  # 'e' key pressed
        elif event.key == pygame.K_1:
            self.game.player.select_skill(0)  # Select first skill
        elif event.key == pygame.K_2:
            self.game.player.select_skill(1)  # Select second skill

    def handle_e_key_press(self):
        # Handle 'e' key press by spawning an enemy
        self.game.spawn_enemy(self.game.player._x, self.game.player._y)
