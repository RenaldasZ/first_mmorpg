# src/game_logic/quest_handler.py
import pygame

class QuestHandler:
    def __init__(self, player, screen_size, screen, item_handler):
        self.screen_size = screen_size
        self.screen = screen
        self.player = player
        self.item_handler = item_handler
        self.font = pygame.font.Font(None, 24)
        self.message_window = pygame.Surface((screen_size[0] // 2, screen_size[1] // 8))
        self.message_rect = self.message_window.get_rect(bottomleft=(screen_size[0] // 2 // 2, screen_size[1]))
        self.load_images()

        # Quest flags
        self.quest_active = False
        self.healing_quest_active = False
        self.axe_head_returned = False
        self.stick_returned = False
        self.empty_vial_returned = False
        self.filled_vial_of_water = False

        # Quest item spawn positions
        self.axe_head_spawn_pos = (4000, 4000)
        self.vial_spawn_pos = (5500, 6000)

    def load_images(self):
        self.axe_head_image = pygame.image.load("assets/quest/axehead.png").convert_alpha()
        self.vial_image = pygame.image.load("assets/quest/vial.png").convert_alpha()

        self.quest_messages = {
            "start": [
                "Hey hero! Got a task for you. \n My axe broke mid-swing in the forest.",
                "I need an axe head and a stick to fix it. \n Yeah, weird, I know. Wanna help?", 
                "Press mouse button to accept this quest. \n Rewards await!"
            ],
            "complete_quest": [
                "Huzzah, adventurer! \n You've found the missing axe head! Amazing job!",
                "Take this Gold Coin as a first reward!",
                "With the axe repaired, we can get back to chopping those trees down! \n But hold on tight, we still need that stick for the axe's full power!",
                "Onward we go, in search of that elusive stick! \n Adventure calls!",
            ],
            "complete_second_part_quest": [
                "Bravo, intrepid adventurer! \n You've returned triumphant, stick in hand!",
                "Your valor knows no bounds! \n Behold, your rewards: a brand spanking new cutting axe!",
                "Now you can chop trees with the finesse of a lumberjack and the style of a knight!",
                "Go forth, mighty one, and let the forests tremble at your approach!",
                "Cutting Axe added to your inventory."
            ],
            "handle_axe_pickup": [
                "You've discovered the missing Axe head! \n Now you can return to woodcutter."
            ],
            "healing_quest_start": [
                "Hey there, hero! Let me teach you how to heal yourself.",
                "Bring me Empty vial"
            ],
            "handle_vial_pickup": [
                "You've discovered Empty vial! \n Now you can return to healer."
            ],
            "bring_empty_vial_quest": [
                "Great, hero. Now fill vial with water."
            ],
            "vial_of_water_returned": [
                "Thank you, hero. Now you'r able to drink from the well and heal yourself."
            ],
        }

    def start_quest(self):
        self.display_messages("start")        
        self.quest_active = True

    def return_axe_head(self):
        if "Axe Head" in self.player.inventory.items:
            self.axe_head_returned = True
            self.complete_quest()
        else:
            self.display_hint("Look southwest for the axe head.")

    def complete_quest(self):
        if self.axe_head_returned:
            self.display_messages("complete_quest")
            self.player.add_to_inventory("Gold Coin")
            self.player.remove_item_from_inventory("Axe Head")

    def return_stick(self):
        if "Stick" in self.player.inventory.items:
            self.stick_returned = True
            self.complete_second_part_quest()
        else:
            self.display_hint("Look for any tree in the world and grab a stick.")

    def handle_axe_pickup(self):
        if self.axe_head_spawn_pos and self.player.rect.colliderect(pygame.Rect(self.axe_head_spawn_pos[0], self.axe_head_spawn_pos[1], 200, 200)):
            self.item_handler.pickup_axe()
            self.axe_head_spawn_pos = None
            self.display_messages("handle_axe_pickup")

        if self.axe_head_spawn_pos:
            screen_pos = (self.axe_head_spawn_pos[0] - self.player._x + self.screen_size[0] // 2,
                          self.axe_head_spawn_pos[1] - self.player._y + self.screen_size[1] // 2)
            self.screen.blit(self.axe_head_image, screen_pos)
            # pygame.display.flip()

    def complete_second_part_quest(self):
        if self.stick_returned:
            self.display_messages("complete_second_part_quest")
            self.player.add_to_inventory("Cutting Axe")
            self.quest_active = False
            self.player.remove_item_from_inventory("Stick")

    def first_quest_completed(self):
        return self.axe_head_returned and self.stick_returned

    def healing_quest_start(self):
        if self.stick_returned:
            self.display_messages("healing_quest_start")        
            self.healing_quest_active = True

    def handle_vial_pickup(self):
        if self.vial_spawn_pos and self.player.rect.colliderect(pygame.Rect(self.vial_spawn_pos[0], self.vial_spawn_pos[1], 200, 200)):
            self.item_handler.pickup_vial()
            self.vial_spawn_pos = None
            self.display_messages("handle_vial_pickup")

        if self.vial_spawn_pos:
            screen_pos = (self.vial_spawn_pos[0] - self.player._x + self.screen_size[0] // 2,
                          self.vial_spawn_pos[1] - self.player._y + self.screen_size[1] // 2)
            self.screen.blit(self.vial_image, screen_pos)
            # pygame.display.flip()

    def return_empty_vial(self):
        if "Empty vial" in self.player.inventory.items:
            self.empty_vial_returned = True
            self.complete_empty_vial_quest()
        else:
            self.display_hint("Hint: Look around till you find empty vial.")

    def complete_empty_vial_quest(self):
        if self.empty_vial_returned:
            self.display_messages("bring_empty_vial_quest")
            self.vial_of_water_quest()

    def vial_of_water_quest(self):
        if "Vial of Water" in self.player.inventory.items:
            self.display_messages("vial_of_water_returned")
            self.healing_quest_active = False
            self.filled_vial_of_water = True
        else:
            self.display_hint("Hint: Use the well to fill the vial with water.")

    def second_quest_completed(self):
        return self.empty_vial_returned and self.filled_vial_of_water

    def display_messages(self, message_type):
        for message in self.quest_messages.get(message_type, []):
            self.display_message(message)

    def display_message(self, message):
        # Display the text message
        self.message_window.fill((0, 0, 0))
        lines = message.split('\n')
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.message_rect.width // 2, 50 + i * 30))
            self.message_window.blit(text_surface, text_rect)

        # Blit the message window onto the screen
        self.fade_in_message()

    def fade_in_message(self):
        alpha = 0
        while alpha <= 255:
            self.message_window.set_alpha(alpha)
            self.screen.blit(self.message_window, self.message_rect)
            alpha += 1

            # Update the display once after all alpha changes
            pygame.display.flip()
            pygame.time.delay(5)

        # Wait for mouse button click to continue
        self.wait_for_click()

    def wait_for_click(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

    def calculate_screen_pos(self, spawn_pos):
        return (spawn_pos[0] - self.player._x + self.screen_size[0] // 2,
                spawn_pos[1] - self.player._y + self.screen_size[1] // 2)

    def display_hint(self, message):
        text_surface = self.font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()