# Maras: The Legacy of Olympus

`Maras` is an open-world MMORPG set in a richly detailed universe inspired by Greek mythology. Developed using the Pygame library in Python, this project aims to provide players with an immersive gaming experience filled with adventure, exploration, and epic battles.

## Key Features:

- **Mythological Realms:** Explore diverse environments based on ancient legends, from the depths of Poseidon's oceanic realm to the towering heights of Mount Olympus.

- **Iconic Characters:** Encounter legendary figures from Greek mythology, including Thor, Poseidon, Hercules, and more, each with unique abilities and quests.

- **Dynamic Gameplay:** Engage in real-time combat against mythical creatures and rival players. Utilize a variety of weapons, spells, and tactics to overcome challenges and emerge victorious.

- **Questing System:** Embark on epic quests that unravel the mysteries of Maras and offer valuable rewards, including powerful artifacts and divine blessings.

- **Player Progression:** Customize your character's skills, abilities, and equipment to suit your playstyle. Advance through levels, unlock new abilities, and become a legendary hero of Maras.

## Development Roadmap:

- **Phase 1: Basic Gameplay Mechanics**
  - Implement player movement, combat mechanics, and interaction with NPCs.
  - Create a basic questing system and world map with initial environments.

- **Phase 2: Expansion of Content**
  - Introduce additional playable characters, enemies, and environments based on player feedback.
  - Enhance combat mechanics with special abilities, combos, and enemy AI improvements.

- **Phase 3: Multiplayer Functionality**
  - Implement networking capabilities for online multiplayer gameplay.
  - Introduce cooperative quests, player-versus-player battles, and social features.

- **Phase 4: Polishing and Optimization**
  - Refine game mechanics, visuals, and user interface for a polished gaming experience.
  - Optimize performance and fix bugs to ensure smooth gameplay on various devices.

## Here's a quick rundown:

**Main Files:**

## Main Files:

- `main.py`: Entry point of the game.
- `map_editor.py`: Module for editing maps, useful during development.

## Assets:

assets/: Directory for storing game assets like images, sounds, etc.

maps/: Directory for storing game maps.

## UI:

- `menu.py`: Module for handling in-game menus.
- `button.py`: Module for creating UI buttons.
- `exit_button_renderer.py`: Renderer module specifically for exit buttons.

## Source Code:

Entities/:

- `enemy.py`: Class definitions for enemies.
- `npc.py`: Class definitions for non-player characters.
- `player.py`: Class definitions for players.

Game Logic/:

- `game.py`: Main game class handling game setup, map loading, player interaction, and enemy spawning.
- `interaction_manager.py`: Manages interactions between game entities and objects.
- `player_manager.py`: Manages player-related logic such as movement, rendering player coordinates and health, and handling player input.
- `quest_handler.py`: Handles quests and quest-related logic for the player.
- `spawn_manager.py`: Manages spawning of enemies and other entities.
- `transition_manager.py`: Manages transitions between game states or maps.

Rendering/:

- `game_renderer.py`: Renders the game world, including players, enemies, NPCs, and objects.
- `map_renderer.py`: Renders the map tiles and objects.
- `player_renderer.py`: Handles rendering specific to player-related UI elements.

Utils/:

- `barrier.py`: Contains functions for detecting collisions with barriers in the game world.
- `item_handler.py`: Manages items within the game, including inventory and item interactions.
- `sprite_sheet.py`: Utility for handling sprite sheets and extracting individual sprites.
- `stack.py`: Implements a stack data structure, potentially used for game mechanics or data handling.

## How to Contribute:

We welcome contributions from developers of all skill levels! If you're interested in contributing to Maras, here's how you can get involved:

1. **Fork the Repository:** Start by forking this repository to your own GitHub account.
2. **Clone the Repository:** Clone your forked repository to your local machine using Git.
3. **Explore the Code:** Take a look at the existing codebase, issues, and project roadmap to get familiar with the project.
4. **Choose an Issue:** Check out the list of open issues and pick one that interests you. Feel free to create new issues or suggest improvements.
5. **Make Changes:** Work on your chosen issue by making changes to the codebase.
6. **Submit a Pull Request:** Once you're done with your changes, submit a pull request to the main repository for review and feedback.

## License:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


Some screenshots from the game:

![alt text](<screenshots/Screenshot 2024-06-27 003724.png>)
![alt text](<screenshots/Screenshot 2024-06-27 003135.png>)
![alt text](<screenshots/Screenshot 2024-06-09 180620.png>)
![alt text](<screenshots/Screenshot 2024-04-12 114947.png>)
![alt text](<screenshots/Screenshot 2024-04-12 115039.png>)
![alt text](<screenshots/Screenshot 2024-04-12 115137.png>)
![alt text](<screenshots/Screenshot 2024-04-12 115211.png>)
![alt text](<screenshots/Screenshot 2024-04-12 115321.png>)

Integrated own map editor:

![alt text](<screenshots/Screenshot 2024-04-12 115713.png>)