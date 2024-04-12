# barrier.py
def collides_with_barrier(pos, map_tiles, CHUNK_SIZE):
    tile_x = int(pos.x // CHUNK_SIZE)
    tile_y = int(pos.y // CHUNK_SIZE)

    if 0 <= tile_y < len(map_tiles) and 0 <= tile_x < len(map_tiles[0]):
        return map_tiles[tile_y][tile_x] == 5

    return False
