import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 71
CARD_HEIGHT = 96
CARD_GAP = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

# Load card images
# You need to have card images stored in a folder named 'cards'
def load_card_images():
    card_images = []
    for i in range(1, 14):
        for suit in ['C', 'D', 'H', 'S']:
            filename = f"cards/{i}{suit}.png"
            image = pygame.image.load(filename).convert_alpha()
            card_images.append(image)
    return card_images

card_images = load_card_images()

# Classes
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

class Deck:
    def __init__(self):
        self.cards = []
        self.populate()
        self.shuffle()

    def populate(self):
        for value in range(1, 14):
            for suit in ['C', 'D', 'H', 'S']:
                self.cards.append(Card(value, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        for card in self.cards:
            if card.value == 1:  # Ace
                if value + 11 <= 21:
                    value += 11
                else:
                    value += 1
            elif card.value >= 10:  # Face cards
                value += 10
            else:
                value += card.value
        return value

# Functions
def draw_card(card, x, y):
    index = (card.value - 1) * 4 + ['C', 'D', 'H', 'S'].index(card.suit)
    image = card_images[index]
    screen.blit(image, (x, y))

def main():
    # Game setup
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Drawing the cards
        screen.fill(GREEN)
        draw_card(player_hand.cards[0], 100, 300)
        draw_card(player_hand.cards[1], 100 + CARD_WIDTH + CARD_GAP, 300)
        draw_card(dealer_hand.cards[0], 100, 100)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
