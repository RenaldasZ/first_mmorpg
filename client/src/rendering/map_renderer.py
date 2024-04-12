# src/rendering/map_rendering.py
import pygame

# Define tile constants
TILE_GRASS_BODY = 2
TILE_TREE = 5
TILE_STONE = 6
TILE_WATERFALL = 7
TILE_WELL = 16
TILE_DARK_GRASS_BODY = 17
TILE_NPC1 = 20
TILE_NPC2 = 21
TILE_BOTTOM = 22
TILE_LEFT = 23
TILE_BOTTOM_LEFT = 24

# Define image paths
IMAGE_PATHS = {
    TILE_GRASS_BODY: 'assets/terrain/grass_body.png',
    TILE_TREE: 'assets/terrain/tree.png',
    TILE_STONE: 'assets/terrain/stone5.png',
    TILE_WATERFALL: 'assets/terrain/waterfall_sprite_sheet.png',
    TILE_BOTTOM: 'assets/terrain/bottom.png',
    TILE_LEFT: 'assets/terrain/left.png',
    TILE_WELL: 'assets/terrain/well.png',
    TILE_DARK_GRASS_BODY: 'assets/terrain/grass_body2.png',
    TILE_NPC1: 'assets/quest/npc1.png',
    TILE_NPC2: 'assets/quest/npc2.png',
    TILE_BOTTOM_LEFT: 'assets/terrain/bottom_left.png'
}

def load_images():
    """Load images for map rendering."""
    images = {}
    for tile_type, path in IMAGE_PATHS.items():
        try:
            images[tile_type] = pygame.image.load(path).convert()
        except pygame.error as e:
            print(f"Error loading image for tile type {tile_type}: {e}")
            # Handle error gracefully, e.g., fallback to a default image
    return images

def render_map(game, viewport_factor=8):
    """Render the game map."""
    screen = game.screen
    player = game.player
    map_tiles = game.map_tiles
    screen_size = game.screen_size
    chunk_size = game.CHUNK_SIZE
    
    player_chunk_x, player_chunk_y = player._x // chunk_size, player._y // chunk_size
    player_offset_x, player_offset_y = player._x % chunk_size, player._y % chunk_size
    
    half_screen_width = screen_size[0] // 2 * viewport_factor
    half_screen_height = screen_size[1] // 2 * viewport_factor
    
    render_start_x = max(0, int(player_chunk_x - half_screen_width // (2 * game.CHUNK_SIZE)))
    render_end_x = min(len(game.map_tiles[0]), int(player_chunk_x + half_screen_width // (2 * game.CHUNK_SIZE) + 1))
    render_start_y = max(0, int(player_chunk_y - half_screen_height // (2 * game.CHUNK_SIZE)))
    render_end_y = min(len(game.map_tiles), int(player_chunk_y + half_screen_height // (2 * game.CHUNK_SIZE) + 1))
    
    center_x = screen_size[0] // 2
    center_y = screen_size[1] // 2
    
    images = load_images()
    
    for y in range(render_start_y, render_end_y):
        for x in range(render_start_x, render_end_x):
            tile_type = map_tiles[y][x]
            if tile_type in images:
                image = images[tile_type]
                screen.blit(image, ((x - player_chunk_x) * chunk_size + center_x - player_offset_x,
                                    (y - player_chunk_y) * chunk_size + center_y - player_offset_y))
