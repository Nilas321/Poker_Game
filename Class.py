from itertools import combinations




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
        #print(game)
        self.flop()
        #print(game)
        self.turn()
        #print(game)
        self.river()
        #print(game)
    
    def get_player_hand(self):
        return self.player_hand

    def get_dealer_hand(self):
        return self.dealer_hand

    def __str__(self):
        return f"Player's Hand: {self.player_hand}\nDealer's Hand: {self.dealer_hand}"
    

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
    for card in card_set:
        suits.add(card.suit)
    if not len(suits) == 1:
        return None
    #print(f"Flush found with cards: {', '.join(str(card) for card in card_set)}")
            
    return "Flush"

def straight(card_set):
    ranks = set()
    baby_straight = False

    for card in card_set:
        ranks.add(card.value)
    
    ranks = sorted(ranks)

    if len(ranks) < 5:
        return None,0
    check_val = ranks[-1] - ranks[0] 
    #print(f"Checking Straight with ranks: {ranks}")
    if ranks == [2,3,4,5,14]:  # Special case for baby straight
        baby_straight = True
        #print("Baby Straight found with cards: 2, 3, 4, 5, Ace")
    elif check_val != 4:
        return None,0
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
def compare_paired(old_hand, new_hand):
    # get the value,no of repeats of each hand
    new_dict = create_dict(new_hand)
    old_dict = create_dict(old_hand)

    new_list = sorted([(key, value) for key, value in new_dict.items()], key=lambda x: (-x[1],x[0]))
    old_list = sorted([(key, value) for key, value in old_dict.items()], key=lambda x: (-x[1],x[0]))
    #print(f"New Hand: {new_list}, Old Hand: {old_list}")
    for i in range(len(new_list)):
        if new_list[i][0] > old_list[i][0]:
            return new_hand
        elif new_list[i][0] < old_list[i][0]:
            return old_hand
        else:
            continue

    return new_hand  # If all cards are equal, return the first hand
    

    
def evaluate_hand(game):
    print("Evaluating Best Hand...")
    # Get all cards from player and dealer hands
    total_cards = game.player_hand.cards + game.dealer_hand.cards
    #total_cards = [card("Queen", "Spades"), card("3", "Hearts"), card("10", "Spades"),
    #              card("King", "Spades"), card("4", "Spades"), card("Jack", "Spades"),
    #             card("Ace", "Spades")]
    print(f"Total Cards: {', '.join(str(card) for card in total_cards)}")
    best_hand = None
    best_set = None
    prev_val = 0
    for fivecardset in combinations(total_cards,5):
        #print(f"Evaluating Hand: {', '.join(str(card) for card in fivecardset)}")
        straight_val = straight(fivecardset)
        temp_hand = pair_analysis(fivecardset)
        is_flush = flush(fivecardset)
        if is_flush and straight_val[1] == 14:
            best_hand = "Royal Flush"
            best_set = fivecardset
            break

        elif is_flush and straight_val[1]:
            if prev_val < straight_val[1]:
                best_hand = "Straight Flush"
                best_set = fivecardset
                prev_val = straight_val[1]
            else:
                continue
        
        elif temp_hand == "Four of a Kind":
            if best_hand != "Straight Flush":
                if best_hand == temp_hand:
                    best_set = compare_paired(best_set, fivecardset)
                    continue
                else:
                    best_hand = temp_hand
                    best_set = fivecardset
                    prev_val = 0
            else:
                continue
        
        elif temp_hand == "Full House":
            if best_hand not in ["Straight Flush", "Four of a Kind"]:
                if best_hand == temp_hand:
                    best_set = compare_paired(best_set, fivecardset)
                    continue
                else:
                    best_hand = temp_hand
                    best_set = fivecardset
                    prev_val = 0
            else:
                continue
        
        elif is_flush == "Flush":
            if best_hand not in ["Straight Flush", "Four of a Kind", "Full House"]:
                if best_hand == "Flush":
                    best_set = compare_flushes(best_set, fivecardset)
                    continue
                else:
                    best_hand = "Flush"
                    best_set = fivecardset
                    prev_val = 0
            else:
                continue
        
        elif straight_val[0]:
            if best_hand not in ["Straight Flush", "Four of a Kind", "Full House", "Flush"]:
                if best_hand == "Straight":
                    if prev_val < straight_val[1]:
                        best_set = fivecardset
                        prev_val = straight_val[1]
                    continue
                else:
                    #print(f"Straight found with value: {straight_val} ")
                    best_hand = "Straight"
                    best_set = fivecardset
                    prev_val = straight_val[1]
            else:
                continue
        
        elif temp_hand == "Three of a Kind":
            if best_hand not in ["Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight"]:
                if best_hand == temp_hand:
                    best_set = compare_paired(best_set, fivecardset)
                    continue
                else:
                    best_hand = temp_hand
                    best_set = fivecardset
                    prev_val = 0
            else:
                continue
        
        elif temp_hand == "Two Pair":
            if best_hand not in ["Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind"]:
                if best_hand == temp_hand:
                    best_set = compare_paired(best_set, fivecardset)
                    continue
                else:
                    best_hand = temp_hand
                    best_set = fivecardset
                    prev_val = 0
            else:
                continue
        
        elif temp_hand == "One Pair":
            if best_hand not in ["Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair"]:
                if best_hand == temp_hand:
                    best_set = compare_paired(best_set, fivecardset)
                    continue
                else:
                    best_hand = temp_hand
                    best_set = fivecardset
                    prev_val = 0
            else:
                continue
        elif temp_hand == "High Card":
            if best_hand not in ["Straight Flush", "Four of a Kind", "Full House", "Flush", "Straight", "Three of a Kind", "Two Pair", "One Pair"]:
                if best_hand == temp_hand:
                    best_set = compare_paired(best_set, fivecardset)
                    continue
                else:
                    best_hand = temp_hand
                    best_set = fivecardset
                    prev_val = 0
            else:
                continue
    
    print(f"Best Hand: {best_hand}")
    print(f"Best Set: {', '.join(str(card) for card in best_set)}")
    
game = Game()
game.play()
evaluate_hand(game)