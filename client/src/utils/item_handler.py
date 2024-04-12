# item_handler.py
class ItemHandler:
    """Handles the logic for picking up items during quests."""
    
    def __init__(self, player):
        """
        Initialize the ItemHandler.

        Args:
            player (Player): The player object to which items will be added.
        """
        self.player = player

    def pickup_axe(self):
        """Pick up the axe item and add it to the player's inventory."""
        quest_item = "Axe Head"  # Example reward
        self.player.add_to_inventory(quest_item)

    def pickup_vial(self):
        """Pick up the vial item and add it to the player's inventory."""
        quest_item = "Empty vial"  # Example reward
        self.player.add_to_inventory(quest_item)