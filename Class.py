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

#function to create a dictionary from a set of cards
def create_dict(card_set):
    card_dict = {}
    for card in card_set:
        if card.value in card_dict:
            card_dict[card.value] += 1
        else:
            card_dict[card.value] = 1
    return card_dict

def flush(card_set):
    suits = set()
    max_rank = 0
    for card in card_set:
        suits.add(card.suit)
    
    if not len(suits) == 1:
        return False

            
    return "Flush",max_rank

def straight(card_set):
    ranks = set()
    baby_straight = False

    for card in card_set:
        ranks.add(card.value)
    
    ranks = sorted(ranks)

    if len(ranks) < 5:
        return False,0

    if ranks == (2,3,4,5,14):  # Special case for baby straight
        baby_straight = True
    elif ranks[-1] - ranks[0] != len(ranks) - 1:
        return False,0

    return "Straight", (max(ranks) if not baby_straight else 5)

#Pair analysis function to count pairs/trips/four of a kind in a hand
#creates a dictionary with card values as keys and their counts as values
#a four of a kind will return a dictionary with one key with value 4 and another key with value 1
# a three of a kind will return a dictionary with one key with value 3 and another key with value 2
# a 2 pair will return a dict with 3 keys
# a single pair will return a dict with 4 keys
# a high card will return a dict with 5 keys

def pair_analysis(card_set):
    pair_dict = create_dict(card_set)

    if len(pair_dict) == 2:
        if 4 in pair_dict.values():
            return "Four of a Kind"
        elif 3 in pair_dict.values():
            return "Full House"

    elif len(pair_dict) == 3:
        if 3 in pair_dict.values():
            return "Three of a Kind"
        else:
            return "Two Pair"
    
    elif len(pair_dict) == 4:
        return "One Pair"
    
    elif len(pair_dict) == 5:
        return "High Card"

#a function to compare 2  card flushes and return the better flush 
def compare_flushes(new_flush, old_flush):
    # Sort both flushes by card value
    new_flush = sorted(new_flush, key=lambda x: x.value, reverse=True)
    old_flush = sorted(old_flush, key=lambda x: x.value, reverse=True)

    for i in range(5):
        if new_flush[i].value > old_flush[i].value:
            return new_flush
        elif new_flush[i].value < old_flush[i].value:
            return old_flush
        else:
            continue

    return new_flush  # If all cards are equal, return the first flush

#compare paired hands
def compare_paired(new_hand, old_hand):
    # get the value,no of repeats of each hand
    new_dict = create_dict(new_hand)
    old_dict = create_dict(old_hand)

    new_list = sorted([(key, value) for key, value in new_dict.items()], key=lambda x: (-x[1],x[0]),reverse=True)
    old_list = sorted([(key, value) for key, value in old_dict.items()], key=lambda x: (-x[1],x[0]),reverse=True)

    for i in range(len(new_list)):
        if new_list[i][0] > old_list[i][0]:
            return new_hand
        elif new_list[i][0] < old_list[i][0]:
            return old_hand

    return new_hand  # If all cards are equal, return the first hand
    

    
def evaluvate_hand(hand):
    total_cards = hand.cards + hand.dealer_hand.cards
    # Placeholder for hand evaluation logic
    # This function should evaluate the hand and return a score or ranking
    return "Hand evaluation logic not implemented yet"

def main():
    game = Game()
    game.play()
    print(game)
