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

class Player():
    def __init__(self,name,chips=1000):
        self.chips = chips
        self.name = name
        self.hand = Hand()
        self.best_set = None
        self.best_hand = None
        self.bet_amount = 0
        self.is_folded = False
        self.is_allin = False
        self.is_call = False

        def get_hand(self):
            return self.hand
        def get_chips(self):
            return self.chips

        def __str__(self):
            return f"Player: {self.name}, Chips: {self.chips}, Hand: {self.hand}"

        def best_set(self,best_set):
            self.best_set = best_set

        def best_hand(self,best_hand):
            self.best_hand = best_hand

        def get_best_set(self):
            return self.best_set
        
        def get_best_hand(self):
            return self.best_hand
        
        
class Game():
    def __init__(self,deck=None,player1 = None,player2 = None):
        self.deck = deck if deck else Deck()
        self.deck.shuffle()
        self.player1 = player1
        self.player2 = player2
        self.dealer_hand = Hand()
        self.pot = 0
        self.state = "continue"  # Game state can be pre_flop, flop, turn, river, showdown
        self.current_bet = 0
        self.check_count = 0  # Count of how many times players have checked in the current round

    def __str__(self):
        return f"Player's Hand: {self.player_hand}\nDealer's Hand: {self.dealer_hand}"


    
def str_to_card(card_str,list=False):
    if not list:
        card_card = ''
        card_suit = ''

        if card_str[0].isdigit():
            card_card = int(card_str[0])
        elif card_str[0].Upper() == "T":
            card_card = 10
        elif card_str[0].Upper() == "J":
            card_card = "Jack"
        elif card_str[0].Upper() == "Q":
            card_card = "Queen"
        elif card_str[0].Upper() == "K":
            card_card = "King"
        elif card_str[0].Upper() == "A":
            card_card = "Ace"
        
        if card_str[1].Upper() == "H":
            card_suit = "Hearts"
        elif card_str[1].Upper() == "D":
            card_suit = "Diamonds"
        elif card_str[1].Upper() == "C":
            card_suit = "Clubs"
        elif card_str[1].Upper() == "S":
            card_suit = "Spades"

        return card(card_card, card_suit)
    
    else:
        card_list = []
        for card_s in card_str:
            print(f"Creating card from string: {card_s}")
            card_card = ''
            card_suit = ''

            if card_s[0].isdigit():
                print(f"Card value is digit: {card_s[0]}")
                card_card = str(card_s[0])
            elif card_s[0].Upper() == "T":
                card_card = "10"
            elif card_s[0].Upper() == "J":
                card_card = "Jack"
            elif card_s[0].Upper() == "Q":
                card_card = "Queen"
            elif card_s[0].Upper() == "K":
                card_card = "King"
            elif card_s[0].Upper() == "A":
                card_card = "Ace"

            if card_s[1].Upper() == "H":
                card_suit = "Hearts"
            elif card_s[1].Upper() == "D":
                card_suit = "Diamonds"
            elif card_s[1].Upper() == "C":
                card_suit = "Clubs"
            elif card_s[1].Upper() == "S":
                card_suit = "Spades"
            print(f"Creating card: {card_card} of {card_suit}")

            card_list.append(card(card_card,card_suit))
        return card_list

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
            return  new_hand,"new_hand"
        elif new_list[i][0] < old_list[i][0]:
            return old_hand,"old_hand"
        else:
            continue

    return new_hand,"Equal"  # If all cards are equal, return the first hand
    

    
def evaluate_hand(game,player):
    print("Evaluating Best Hand...")
    # Get all cards from player and dealer hands
    total_cards = player.hand.cards + game.dealer_hand.cards
    #total_cards = [card("Queen", "Spades"), card("3", "Hearts"), card("10", "Spades"),
    #              card("King", "Spades"), card("4", "Spades"), card("Jack", "Spades"),
    #             card("Ace", "Spades")]
    #total_cards = str_to_card(["QH", "3H", "TS", "KS", "QS", "JS", "AS"], list=True)
    print(f"Total Cards: {', '.join(str(card) for card in player.hand.cards)} + {', '.join(str(card) for card in game.dealer_hand.cards)}")
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
                    best_set = compare_paired(best_set, fivecardset)[0]
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
                    best_set = compare_paired(best_set, fivecardset)[0]
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
                    best_set = compare_paired(best_set, fivecardset)[0]
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
                    best_set = compare_paired(best_set, fivecardset)[0]
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
                    best_set = compare_paired(best_set, fivecardset)[0]
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
                    best_set = compare_paired(best_set, fivecardset)[0]
                    continue
                else:
                    best_hand = temp_hand
                    best_set = fivecardset
                    prev_val = 0
            else:
                continue
    
    best_set = sorted(best_set,key = lambda x:x.value,reverse=True)
    print(f"Best Hand: {best_hand}")
    print(f"Best Set: {', '.join(str(card) for card in best_set)}")
    player.best_set =best_set
    player.best_hand =best_hand

def compare_players(player1, player2,game):
    ranking = enumerate(["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"])
    #higher the ranking, better the hand
    rank_dict = {hand: rank for rank, hand in ranking}
    rank_p1 = rank_dict[player1.best_hand]
    rank_p2 = rank_dict[player2.best_hand]
    if rank_p1 > rank_p2:
        player1.chips += game.pot
        print(f"{player1.name} wins with {player1.best_hand}!")
        return 
    elif rank_p1 < rank_p2:
        player2.chips += game.pot
        print(f"{player2.name} wins with {player2.best_hand}!")
        return
    else:
        if rank_p2 == rank_p1 == 9:#Royal Flush"
            player1.chips += game.pot // 2
            player2.chips += game.pot // 2
            print("It's a tie!")
            return
        elif rank_p2 == rank_p1 == 8:#"Straight Flush"
            straight_p1 = straight(player1.best_set)
            straight_p2 = straight(player2.best_set)
            if straight_p1[1] > straight_p2[1]:
                player1.chips += game.pot
                print(f"{player1.name} wins with {player1.best_hand}!")
                return
            elif straight_p1[1] < straight_p2[1]:
                player2.chips += game.pot
                print(f"{player2.name} wins with {player2.best_hand}!")
                return
            else:
                print("It's a tie!")
                return
        elif rank_p2 == rank_p1 == 7:#"Four of a Kind"
            if compare_paired(player1.best_set, player2.best_set)[1] == "Equal":
                player1.chips += game.pot // 2
                player2.chips += game.pot // 2
                print("It's a tie!")
                return
            elif compare_paired(player1.best_set, player2.best_set)[1] == "old_hand":
                player1.chips += game.pot
                print(f"{player1.name} wins with {player1.best_hand}!")
                return
            elif compare_paired(player1.best_set, player2.best_set)[1] == "new_hand":
                player2.chips += game.pot
                print(f"{player2.name} wins with {player2.best_hand}!")
                return
            
        elif rank_p2 == rank_p1 == 6:#"Full House"
            if compare_paired(player1.best_set, player2.best_set)[1] == "Equal":
                player1.chips += game.pot // 2
                player2.chips += game.pot // 2
                print("It's a tie!")
                return
            elif compare_paired(player1.best_set, player2.best_set)[1] == "old_hand":
                player1.chips += game.pot
                print(f"{player1.name} wins with {player1.best_hand}!")
                return
            elif compare_paired(player1.best_set, player2.best_set)[1] == "new_hand":
                player2.chips += game.pot
                print(f"{player2.name} wins with {player2.best_hand}!")
                return
        elif rank_p2 == rank_p1 == 5:#"Flush"
            if compare_flushes(player1.best_set, player2.best_set)[1] == "Equal":
                player1.chips += game.pot // 2
                player2.chips += game.pot // 2
                print("It's a tie!")
                return
            elif compare_flushes(player1.best_set, player2.best_set)[1] == "old_hand":
                player1.chips += game.pot
                print(f"{player1.name} wins with {player1.best_hand}!")
                return
            elif compare_flushes(player1.best_set, player2.best_set)[1] == "new_hand":
                player2.chips += game.pot
                print(f"{player2.name} wins with {player2.best_hand}!")
                return
        elif rank_p2 == rank_p1 == 4:#"Straight"
            if straight(player1.best_set)[1] > straight(player2.best_set)[1]:
                player1.chips += game.pot
                print(f"{player1.name} wins with {player1.best_hand}!")
                return
            elif straight(player1.best_set)[1] < straight(player2.best_set)[1]:
                player2.chips += game.pot
                print(f"{player2.name} wins with {player2.best_hand}!")
                return
            else:
                player1.chips += game.pot // 2
                player2.chips += game.pot // 2
                print("It's a tie!")
                return
        elif rank_p2 == rank_p1 == 3:#"Three of a Kind"
            if compare_paired(player1.best_set, player2.best_set)[1] == "Equal":
                player1.chips += game.pot // 2
                player2.chips += game.pot // 2
                print("It's a tie!")
                return 
            elif compare_paired(player1.best_set, player2.best_set)[1] == "old_hand":
                player1.chips += game.pot
                print(f"{player1.name} wins with {player1.best_hand}!")
                return
            elif compare_paired(player1.best_set, player2.best_set)[1] == "new_hand":
                player2.chips += game.pot
                print(f"{player2.name} wins with {player2.best_hand}!")
                return
        elif rank_p2 == rank_p1 == 2:#"Two Pair"
            if compare_paired(player1.best_set, player2.best_set)[1] == "Equal":
                player1.chips += game.pot // 2
                player2.chips += game.pot // 2
                print("It's a tie!")
                return
            elif compare_paired(player1.best_set, player2.best_set)[1] == "old_hand":
                player1.chips += game.pot
                print(f"{player1.name} wins with {player1.best_hand}!")
                return
            elif compare_paired(player1.best_set, player2.best_set)[1] == "new_hand":
                player2.chips += game.pot
                print(f"{player2.name} wins with {player2.best_hand}!")
                return
        elif rank_p2 == rank_p1 == 1:#"One Pair"
            if compare_paired(player1.best_set, player2.best_set)[1] == "Equal":
                player1.chips += game.pot // 2
                player2.chips += game.pot // 2
                print("It's a tie!")
                return
            elif compare_paired(player1.best_set, player2.best_set)[1] == "old_hand":
                player1.chips += game.pot
                print(f"{player1.name} wins with {player1.best_hand}!")
                return
            elif compare_paired(player1.best_set, player2.best_set)[1] == "new_hand":
                player2.chips += game.pot
                print(f"{player2.name} wins with {player2.best_hand}!")
                return
        elif rank_p2 == rank_p1 == 0:#"High Card"
            if compare_paired(player1.best_set, player2.best_set)[1] == "Equal":
                player1.chips += game.pot // 2
                player2.chips += game.pot // 2
                print("It's a tie!")
                return
            elif compare_paired(player1.best_set, player2.best_set)[1] == "old_hand":
                player1.chips += game.pot
                print(f"{player1.name} wins with {player1.best_hand}!")
                return
            elif compare_paired(player1.best_set, player2.best_set)[1] == "new_hand":
                player2.chips += game.pot
                print(f"{player2.name} wins with {player2.best_hand}!")
            return
        else:
            print("Unexpected case encountered!")
            return


