import pygame
import sys
from ui.menu import Menu
from src.game_logic.game import Game

def initialize_pygame():
    pygame.init()
    screen_info = pygame.display.Info()
    SCREEN_SIZE = (screen_info.current_w, screen_info.current_h)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Map Chunk Rendering")
    return SCREEN_SIZE, screen

def handle_menu_choice(menu, choice):
    if choice == "play":
        return False
    elif choice == "exit":
        exit_game()

def update_fps_text(font, clock, game):
    fps_text = font.render("FPS: " + str(int(clock.get_fps())), True, (0, 0, 0))
    text_rect = fps_text.get_rect()
    text_rect.bottomright = game.screen.get_rect().bottomright
    game.screen.blit(fps_text, text_rect)

def run_game_loop(game, menu):
    clock = pygame.time.Clock()
    show_menu = True
    font = pygame.font.Font(None, 36)

    while game.running:
        if show_menu:
            choice = menu_loop(menu)
            show_menu = handle_menu_choice(menu, choice)
        else:
            game.handle_events()
            game.update()
            game.render()

        clock.tick(60)
        update_fps_text(font, clock, game)
        pygame.display.flip()

def menu_loop(menu):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
        
        menu.render()
        pygame.display.flip()
        choice = menu.handle_events()
        if choice:
            return choice

def exit_game():
    pygame.quit()
    sys.exit()

def main():
    SCREEN_SIZE, screen = initialize_pygame()
    game = Game(SCREEN_SIZE, screen)
    menu = Menu(screen)
    run_game_loop(game, menu)

if __name__ == "__main__":
    main()
