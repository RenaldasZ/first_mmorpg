# exit_button_renderer.py
def is_exit_button_clicked(mouse_pos, font, screen_size):
    # Define the exit button's position and dimensions
    exit_text_surface = font.render("Exit Game", True, (0, 0, 0))
    exit_text_rect = exit_text_surface.get_rect()
    exit_text_rect.topleft = (screen_size[0] - exit_text_rect.width - 20, 10)
    exit_button_rect = exit_text_rect.inflate(10, 10)

    # Check if the mouse click is within the exit button's bounds
    return exit_button_rect.collidepoint(mouse_pos)