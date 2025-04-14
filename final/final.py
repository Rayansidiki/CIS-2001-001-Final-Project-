import random

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
            value += 11 if value + 11 <= 21 else 1
        return value

    def __repr__(self):
        return f"{self.name} hand: {self.hand} | Value: {self.get_hand_value()}"

# Dealer Class
class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")

    def should_hit(self):
        return self.get_hand_value() < 17

# Blackjack Game Function
def play_blackjack():
    shoe = Shoe()
    player = Player("Player")
    dealer = Dealer()

    # Deal initial hands
    player.add_card(shoe.deal())
    dealer.add_card(shoe.deal())
    player.add_card(shoe.deal())
    dealer.add_card(shoe.deal())

    print("\nInitial hands:")
    print(player)
    print(f"Dealer shows: {dealer.hand[0]}")

    # Player's turn
    while True:
        action = input("Hit or stand? (h/s): ").lower()
        if action not in ['h', 's']:
            print("Please enter 'h' or 's'")
            continue
        if action == 'h':
            player.add_card(shoe.deal())
            print(player)
            if player.get_hand_value() > 21:
                print("Player busts! Dealer wins.\n")
                return
        else:
            break

    # Dealer's turn
    print("\nDealer's turn:")
    print(dealer)
    while dealer.should_hit():
        dealer.add_card(shoe.deal())
        print(dealer)
        if dealer.get_hand_value() > 21:
            print("Dealer busts! Player wins.\n")
            return

    # Determine winner
    player_val = player.get_hand_value()
    dealer_val = dealer.get_hand_value()
    print()
    if player_val > dealer_val:
        print("Player wins!\n")
    elif player_val < dealer_val:
        print("Dealer wins!\n")
    else:
        print("It's a tie!\n")

if __name__ == "__main__":
    while True:
        play_blackjack()
        again = input("Play again? (y/n): ").lower()
        if again != 'y':
            print("Thanks for playing!")
            break
