# src/game_logic/transition_manager.py
import json

class TransitionManager:
    def __init__(self, game):
        self.game = game

    def transition_to_second_map(self):
        if not self.game.transitioning:
            self.load_map('maps/map2.json')
            self.game.spawn_manager.spawn_enemies_second_map()
            self.game.player.position = (9800, 9800)
            self.game.transitioning = True
            item = "Health Potion"
            self.game.player.add_to_inventory(item)

    def load_map(self, map_filename):
        try:
            with open(map_filename, 'r') as f:
                self.game.map_tiles = json.load(f)
        except FileNotFoundError:
            print(f"Error: Map file '{map_filename}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in map file '{map_filename}'.")
