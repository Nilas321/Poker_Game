class card():
    def __init__(self,card,suit):
        self.card = card
        self.suit = suit
        pass

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
        for _ in range(1):
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

def flush(card_set,player_hand):
    suits = set()
    max_rank = 0
    for card in card_set:
        suits.add(card.suit)
    
    if not len(suits) == 1:
        return False

    for card in player_hand.cards:
        if card in card_set:
            rank = card.card
            if rank.isdigit():
                max_rank = max(max_rank,int(rank))
            elif rank in ["Jack", "Queen", "King"]:
                max_rank = max(max_rank,11 + ["Jack", "Queen", "King"].index(rank))
            else:
                max_rank = 14  # Ace is the highest rank
            
    return (len(suits) == 1, max_rank)

def straight(card_set, player_hand):
    ranks = set()
    max_rank = 0
    baby_straight = False

    for card in card_set:
        if card.card.isdigit():
            ranks.add(int(card.card))
        elif card.card in ["Jack", "Queen", "King"]:
            ranks.add(10 + ["Jack", "Queen", "King"].index(card.card))
        else:
            ranks.add(14)  # Ace is the highest rank

    
    

    ranks = sorted(ranks)

    if ranks == (2,3,4,5,14):  # Special case for baby straight
        baby_straight = True

    elif ranks[-1] - ranks[0] != len(ranks) - 1:
        return False


    for card in player_hand.cards:
        if card in card_set:
            rank = card.card
            if rank.isdigit():
                max_rank = max(max_rank,int(rank))
            elif rank in ["Jack", "Queen", "King"]:
                max_rank = max(max_rank,11 + ["Jack", "Queen", "King"].index(rank))
            else:
                if rank == "Ace":
                    if baby_straight:
                        max_rank = max(max_rank, 1)  # Ace counts as 1 in baby straight

                else:
                    max_rank = 14
    return False

def evaluvate_hand(hand):
    total_cards = hand.cards + hand.dealer_hand.cards
    # Placeholder for hand evaluation logic
    # This function should evaluate the hand and return a score or ranking
    return "Hand evaluation logic not implemented yet"

def main():
    game = Game()
    game.play()
    print(game)
