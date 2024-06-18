# src/game_logic/interaction_manager.py
class InteractionManager:
    def __init__(self, game):
        self.game = game

    def handle_well_interaction(self):
        self.game.player.heal(0.1)
        if "Empty vial" in self.game.player.inventory.items and self.game.quest_handler.empty_vial_returned:
            self.game.player.remove_item_from_inventory("Empty vial")
            self.game.player.add_to_inventory("Vial of Water")

    def handle_tree_interaction(self):
        if "Stick" not in self.game.player.inventory.items:
            self.game.player.add_to_inventory("Stick")

    def check_interaction(self):
        # Get the player's position in terms of chunks
        player_x_chunk = int((self.game.player._x + self.game.player._size / 2) // self.game.CHUNK_SIZE)
        player_y_chunk = int((self.game.player._y + self.game.player._size / 2) // self.game.CHUNK_SIZE)

        # Define the range of chunks to check around the player
        chunk_range = range(player_x_chunk - 1, player_x_chunk + 1)
        chunk_range_y = range(player_y_chunk - 1, player_y_chunk + 1)

        # Iterate over the surrounding chunks to check for interactions
        for chunk_x in chunk_range:
            for chunk_y in chunk_range_y:
                # Ensure chunk indices are within bounds of the map
                if 0 <= chunk_x < len(self.game.map_tiles[0]) and 0 <= chunk_y < len(self.game.map_tiles):
                    # Handle well interaction
                    if self.game.map_tiles[chunk_y][chunk_x] == self.game.TILE_WELL:
                        self.handle_well_interaction()
                        return
                    # Handle tree interaction
                    elif self.game.map_tiles[chunk_y][chunk_x] == self.game.TILE_TREE:
                        self.handle_tree_interaction()
                        return
