# src/entities/npc.py

class NPC:
    """
    Represents non-player characters (NPCs) in the game, handling interactions and quests.
    """
    TILE_NPC_1 = 20
    TILE_NPC_2 = 21

    # NPC positions (x, y) in the map
    POSITIONS = {
        TILE_NPC_1: (5280, 4850),
        TILE_NPC_2: (5680, 3850),
    }

    def __init__(self, quest_handler):
        """
        Initialize the NPC instance.

        Args:
            quest_handler (QuestHandler): The handler for managing quests.
        """
        self.quest_handler = quest_handler

    def handle_interaction(self, player, tile_id):
        """
        Handle interaction with an NPC based on the tile ID.

        Args:
            player (Player): The player interacting with the NPC.
            tile_id (int): The tile ID of the NPC being interacted with.
        """
        if tile_id == self.TILE_NPC_1:
            self._handle_npc1_interaction(player)
        elif tile_id == self.TILE_NPC_2:
            self._handle_npc2_interaction(player)

    def _handle_npc1_interaction(self, player):
        """
        Handle the specific interaction logic for NPC 1.

        Args:
            player (Player): The player interacting with NPC 1.
        """
        if not self.quest_handler.quest_active and not self.quest_handler.axe_head_returned:
            self.quest_handler.start_quest()
        elif self.quest_handler.quest_active and not self.quest_handler.axe_head_returned:
            self.quest_handler.return_axe_head()
        elif self.quest_handler.axe_head_returned and not self.quest_handler.stick_returned:
            self.quest_handler.return_stick()

    def _handle_npc2_interaction(self, player):
        """
        Handle the specific interaction logic for NPC 2.

        Args:
            player (Player): The player interacting with NPC 2.
        """
        if not self.quest_handler.healing_quest_active and not self.quest_handler.empty_vial_returned:
            self.quest_handler.healing_quest_start()
        elif self.quest_handler.healing_quest_active and not self.quest_handler.empty_vial_returned:
            self.quest_handler.return_empty_vial()
        elif self.quest_handler.healing_quest_active and not self.quest_handler.filled_vial_of_water:
            self.quest_handler.vial_of_water_quest()
