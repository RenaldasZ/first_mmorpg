# src/game_logic/interaction_manager.py
import math

class InteractionManager:
    """
    Manages player interactions with objects in the game world.
    """

    INTERACTION_DISTANCE = 150  # The distance within which the player can interact with objects

    def __init__(self, game):
        """
        Initializes the InteractionManager.

        Args:
            game (Game): The game instance.
        """
        self.game = game

    def handle_well_interaction(self) -> None:
        """
        Handles interaction with a well, healing the player and possibly converting an empty vial to a vial of water.
        """
        self.game.player.heal(0.1)
        if "Empty vial" in self.game.player.inventory.items and self.game.quest_handler.empty_vial_returned:
            self.game.player.remove_item_from_inventory("Empty vial")
            self.game.player.add_to_inventory("Vial of Water")

    def handle_tree_interaction(self) -> None:
        """
        Handles interaction with a tree, adding a stick to the player's inventory if not already present.
        """
        if "Stick" not in self.game.player.inventory.items:
            self.game.player.add_to_inventory("Stick")

    def is_within_distance(self, target_x: float, target_y: float, distance: float) -> bool:
        """
        Determines if the player is within a certain distance from a target.

        Args:
            target_x (float): The x-coordinate of the target.
            target_y (float): The y-coordinate of the target.
            distance (float): The distance to check.

        Returns:
            bool: True if within distance, False otherwise.
        """
        return math.hypot(self.game.player._x - target_x, self.game.player._y - target_y) <= distance

    def check_interaction(self) -> None:
        """
        Checks for player interactions with nearby objects such as wells or trees.
        """
        # Get the player's position in terms of chunks
        player_x_chunk = int((self.game.player._x + self.game.player._size / 2) // self.game.CHUNK_SIZE)
        player_y_chunk = int((self.game.player._y + self.game.player._size / 2) // self.game.CHUNK_SIZE)
        
        # Define the range of chunks to check around the player
        chunk_range = range(player_x_chunk - 1, player_x_chunk + 2)
        chunk_range_y = range(player_y_chunk - 1, player_y_chunk + 2)

        # Iterate over the surrounding chunks to check for interactions
        for chunk_x in chunk_range:
            for chunk_y in chunk_range_y:
                # Ensure chunk indices are within bounds of the map
                if 0 <= chunk_x < len(self.game.map_tiles[0]) and 0 <= chunk_y < len(self.game.map_tiles):
                    tile = self.game.map_tiles[chunk_y][chunk_x]
                    target_x = chunk_x * self.game.CHUNK_SIZE + self.game.CHUNK_SIZE // 2
                    target_y = chunk_y * self.game.CHUNK_SIZE + self.game.CHUNK_SIZE // 2
                    
                    if tile == self.game.TILE_WELL and self.is_within_distance(target_x, target_y, self.INTERACTION_DISTANCE):
                        self.handle_well_interaction()
                        return
                    elif tile == self.game.TILE_TREE and self.is_within_distance(target_x, target_y, self.INTERACTION_DISTANCE):
                        self.handle_tree_interaction()
                        return
