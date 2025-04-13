import random

# Card Class
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

# Deck Class
class Deck:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self):
        self.cards = [Card(suit, value) for suit in Deck.suits for value in Deck.values]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

# Shoe Class
class Shoe:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.cards = []
        self.reshuffle()

    def reshuffle(self):
        self.cards = []
        for _ in range(self.num_decks):
            deck = Deck()
            deck.shuffle()
            self.cards.extend(deck.cards)
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) < 100:
            self.reshuffle()
        return self.cards.pop()

# Player Class
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def get_hand_value(self):
        value = 0
        aces = 0
        for card in self.hand:
            if card.value in ["J", "Q", "K"]:
                value += 10
            elif card.value == "A":
                aces += 1
            else:
                value += int(card.value)
        for _ in range(aces):
            if value + 11 <= 21:
                value += 11
            else:
                value += 1
        return value

    def __repr__(self):
        return f"Player {self.name} with hand {self.hand} and value {self.get_hand_value()}"

# Dealer Class
class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")

    def should_hit(self):
        return self.get_hand_value() < 17

# Example of how to use these classes to start a game of Blackjack
def play_blackjack():
    shoe = Shoe()
    player = Player("Player 1")
    dealer = Dealer()

    # Deal initial cards
    player.add_card(shoe.deal())
    dealer.add_card(shoe.deal())
    player.add_card(shoe.deal())
    dealer.add_card(shoe.deal())

    print("Initial hands:")
    print(player)
    print(dealer)

    # Player's turn
    while True:
        action = input("Do you want to hit or stand? (h/s): ")
        if action.lower() == 'h':
            player.add_card(shoe.deal())
            print(player)
            if player.get_hand_value() > 21:
                print("Bust! Dealer wins.")
                return
        else:
            break

    # Dealer's turn
    while dealer.should_hit():
        dealer.add_card(shoe.deal())
        print(dealer)
        if dealer.get_hand_value() > 21:
            print("Dealer busts! Player wins.")
            return

    # Determine the winner
    if player.get_hand_value() > dealer.get_hand_value():
        print("Player wins!")
    elif player.get_hand_value() < dealer.get_hand_value():
        print("Dealer wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_blackjack()