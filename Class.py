class card():
    def __init__(self,card,suit):
        self.card = card
        self.suit = suit
        self.value = self.get_value()
        pass

    def get_value(self):
        if self.card.isdigit():
            return int(self.card)
        elif self.card in ["Jack", "Queen", "King"]:
            return 11 + ["Jack", "Queen", "King"].index(self.card)
        elif self.card == "Ace":
            return 14

    def __str__(self):
        return f"{self.card} of {self.suit}"
    

class Deck():
    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        for suit in suits:
            for card_no in cards:
                self.cards.append(card(card_no, suit))
    
    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
    

class Hand():
    def __init__(self):
        self.cards = []
        self.number_of_cards = len(self.cards)


    def dealt_card(self, card):
        self.cards.append(card)

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
    
class Game():
    def __init__(self,deck=None):
        self.deck = deck if deck else Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def deal(self):
        for _ in range(2):  # Deal two cards to each player
            self.player_hand.dealt_card(self.deck.cards.pop())
    
    def flop(self):
        for _ in range(3):
            self.dealer_hand.dealt_card(self.deck.cards.pop())
    
    def turn(self):
        self.dealer_hand.dealt_card(self.deck.cards.pop())

    
    def river(self):
            self.dealer_hand.dealt_card(self.deck.cards.pop())

    def play(self):
        self.deal()
        print(game)
        self.flop()
        print(game)
        self.turn()
        print(game)
        self.river()
        print(game)
    
    def get_player_hand(self):
        return self.player_hand

    def get_dealer_hand(self):
        return self.dealer_hand

    def __str__(self):
        return f"Player's Hand: {self.player_hand}\nDealer's Hand: {self.dealer_hand}"
    
if __name__ == "__main__":
    game = Game()
    game.play()
    print(game)
    print("Player's Hand:", game.get_player_hand())
    print("Dealer's Hand:", game.get_dealer_hand())
    print("Deck after dealing:", game.deck)
    print("Remaining cards in deck:", len(game.deck.cards))

# This code defines a simple poker game structure with classes for cards, decks, hands, and the game itself.

def flush(card_set):
    suits = set()
    max_rank = 0
    for card in card_set:
        suits.add(card.suit)
    
    if not len(suits) == 1:
        return False

            
    return "Flush"

def straight(card_set):
    ranks = set()
    max_rank = 0
    baby_straight = False

    for card in card_set:
        ranks.add(card.value)
    
    ranks = sorted(ranks)

    if len(ranks) < 5:
        return False,0

    if ranks == (2,3,4,5,14):  # Special case for baby straight
        baby_straight = True
    elif ranks[-1] - ranks[0] != len(ranks) - 1:
        return False

    return "Straight"

#Pair analysis function to count pairs/trips/four of a kind in a hand
#creates a dictionary with card values as keys and their counts as values
#a four of a kind will return a dictionary with one key with value 4 and another key with value 1
# a three of a kind will return a dictionary with one key with value 3 and another key with value 2
# a 2 pair will return a dict with 3 keys
# a single pair will return a dict with 4 keys
# a high card will return a dict with 5 keys

def pair_analysis(card_set):
    pair_dict = {}
    for card in card_set:
        if card.value in pair_dict:
            pair_dict[card.value] += 1
        else:
            pair_dict[card.value] = 1
    
    if len(pair_dict) == 2:
        if 4 in pair_dict.values():
            return "Four of a Kind"
        elif 3 in pair_dict.values():
            return "Three of a Kind"
        return 
    elif len(pair_dict) == 3:
        return "Two Pair"
    
    elif len(pair_dict) == 4:
        return "One Pair"
    
    elif len(pair_dict) == 5:
        return "High Card"


def evaluvate_hand(hand):
    total_cards = hand.cards + hand.dealer_hand.cards
    # Placeholder for hand evaluation logic
    # This function should evaluate the hand and return a score or ranking
    return "Hand evaluation logic not implemented yet"

def main():
    game = Game()
    game.play()
    print(game)
