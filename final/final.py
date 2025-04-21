import random
from collections import defaultdict

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
        self.cards = [Card(s, v) for s in Deck.suits for v in Deck.values]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

class Shoe:
    def __init__(self, num_decks=6):
        self.cards = []
        self.num_decks = num_decks
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

    def reset(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        value, aces = 0, 0
        for card in self.hand:
            if card.value in ['J', 'Q', 'K']:
                value += 10
            elif card.value == 'A':
                aces += 1
            else:
                value += int(card.value)
        for _ in range(aces):
            value += 11 if value + 11 <= 21 else 1
        return value

    def show_hand(self):
        return ', '.join(str(card) for card in self.hand)

class Dealer(Player):
    def __init__(self):
        super().__init__('Dealer')

    def should_hit(self):
        return self.get_value() < 17

def play_game():
    shoe = Shoe()
    player = Player('Player')
    dealer = Dealer()
    balance = 0

    while True:
        player.reset()
        dealer.reset()

        for _ in range(2):
            player.add_card(shoe.deal())
            dealer.add_card(shoe.deal())

        print("\n--- New Round ---")
        print('Your hand:', player.show_hand(), '| Value:', player.get_value())
        print('Dealer shows:', dealer.hand[0])

        while True:
            action = input('Hit or stand? (h/s): ').lower()
            if action == 'h':
                player.add_card(shoe.deal())
                print('Your hand:', player.show_hand(), '| Value:', player.get_value())
                if player.get_value() > 21:
                    print('Bust! You lose.')
                    balance -= 1
                    break
            elif action == 's':
                break
            else:
                print("Invalid input. Use 'h' or 's'.")

        if player.get_value() <= 21:
            print("\nDealer's turn...")
            print('Dealer hand:', dealer.show_hand(), '| Value:', dealer.get_value())
            while dealer.should_hit():
                dealer.add_card(shoe.deal())
                print('Dealer hits:', dealer.show_hand(), '| Value:', dealer.get_value())

            pv, dv = player.get_value(), dealer.get_value()
            if dv > 21 or pv > dv:
                print('You win!')
                balance += 1
            elif pv < dv:
                print('Dealer wins!')
                balance -= 1
            else:
                print("It's a tie.")

        print(f"Current Balance: ${balance}")
        again = input("Play again? (y/n): ").lower()
        if again != 'y':
            print('Thanks for playing!')
            break

def simulate_strategy():
    shoe = Shoe()
    results = defaultdict(lambda: {'hit': {'W': 0, 'L': 0, 'T': 0},
                                   'stand': {'W': 0, 'L': 0, 'T': 0}})
    total = {'W': 0, 'L': 0, 'T': 0}

    def resolve(player, dealer):
        pv = player.get_value()
        if pv > 21:
            return 'L'
        while dealer.should_hit():
            dealer.add_card(shoe.deal())
        dv = dealer.get_value()
        if dv > 21 or pv > dv:
            return 'W'
        elif pv < dv:
            return 'L'
        return 'T'

    for _ in range(100000):
        player = Player("Sim")
        dealer = Dealer()
        player.reset()
        dealer.reset()
        for _ in range(2):
            player.add_card(shoe.deal())
            dealer.add_card(shoe.deal())

        pv = player.get_value()
        up = dealer.hand[0].value
        try:
            dv = 11 if up == 'A' else (10 if up in ['J', 'Q', 'K'] else int(up))
        except:
            continue
        if pv < 4 or pv > 21:
            continue

        action = random.choice(['hit', 'stand'])
        if action == 'hit':
            player.add_card(shoe.deal())

        outcome = resolve(player, dealer)
        results[(pv, dv)][action][outcome] += 1
        total[outcome] += 1

    print("\n--- Simulation Results (100,000 rounds) ---")
    for key in sorted(results.keys()):
        p, d = key
        hit = results[key]['hit']
        stand = results[key]['stand']
        print(f"P:{p} vs D:{d} | Hit → W:{hit['W']} L:{hit['L']} T:{hit['T']} | Stand → W:{stand['W']} L:{stand['L']} T:{stand['T']}")
    print(f"\nTotal Results → Wins: {total['W']} | Losses: {total['L']} | Ties: {total['T']}")

if __name__ == "__main__":
    mode = input("Type 'play' to play the game or 'sim' to run simulation: ").lower()
    if mode == 'play':
        play_game()
    elif mode == 'sim':
        simulate_strategy()
    else:
        print("Invalid mode.")