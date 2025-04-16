import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self):
        self.cards = [Card(suit, value) for suit in Deck.suits for value in Deck.values]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

class Shoe:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.cards = []
        self.reshuffle()

    def reshuffle(self):
        self.cards = []
        for _ in range(self.num_decks):
            deck = Deck()
            self.cards.extend(deck.cards)
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) < 100:
            self.reshuffle()
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def reset_hand(self):
        self.hand = []

    def get_hand_value(self):
        value, aces = 0, 0
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

    def __str__(self):
        cards = ', '.join(str(card) for card in self.hand)
        return f"{self.name}'s hand: [{cards}] | Value: {self.get_hand_value()}"

class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")

    def should_hit(self):
        return self.get_hand_value() < 17

def play_blackjack():
    shoe = Shoe()
    player = Player("Player")
    dealer = Dealer()

    while True:
        player.reset_hand()
        dealer.reset_hand()

        for _ in range(2):
            player.add_card(shoe.deal())
            dealer.add_card(shoe.deal())

        print("\n--- New Round ---")
        print(player)
        print(f"Dealer shows: {dealer.hand[0]}")

        while player.get_hand_value() < 21:
            action = input("Hit or stand? (h/s): ").lower()
            if action == 'h':
                player.add_card(shoe.deal())
                print(player)
            elif action == 's':
                break
            else:
                print("Please enter 'h' or 's'.")

        if player.get_hand_value() > 21:
            print("Player busts! Dealer wins.\n")
        else:
            print("\nDealer's turn:")
            print(dealer)
            while dealer.should_hit():
                dealer.add_card(shoe.deal())
                print(dealer)

            p_val = player.get_hand_value()
            d_val = dealer.get_hand_value()

            if d_val > 21:
                print("Dealer busts! Player wins.\n")
            elif p_val > d_val:
                print("Player wins!\n")
            elif p_val < d_val:
                print("Dealer wins!\n")
            else:
                print("It's a tie!\n")

        again = input("Play again? (y/n): ").lower()
        if again != 'y':
            print("Thanks for playing!")
            break
