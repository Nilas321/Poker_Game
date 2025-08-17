#creating the poker game

#pre_flop
#actions - check (bet,0) , - bet(bet,x) . - raise_to(bet, y > x),call (bet,x-z), fold(give up the money) all_in (bet , chips)
def bet(player, amount, game):
    """Player bets a certain amount."""
    if player.chips >= amount:
        player.chips -= amount
        game.pot += amount
        game.current_bet = amount
        print(f"{player.name} bets {amount}. Current pot: {game.pot}")
    else:
        print(f"{player.name} does not have enough chips to bet {amount}.")

def action(player,game):
    if game.current_bet == 0:
        # Player can check,bet or fold
        while True:
            action = input(f"{player.name}, do you want to check, bet, or fold? (c/b/f): ").strip().lower()
            if action == 'f':
                player.fold()
                break
            elif action == 'b':
                amount_bet = input(f"{player.name}, enter the amount to bet: ")
                if amount_bet.isdigit():
                    amount_bet = int(amount_bet)
                    if amount_bet > 0 and amount_bet <= player.chips:
                        bet(player, amount_bet, game)
                    elif amount_bet <= 0:
                        print("Bet amount must be greater than 0.")
                    elif amount_bet > player.chips:
                        print(f"{player.name} does not have enough chips to bet {amount_bet}.Do you want to go all in? (y/n)")
                        if input().strip().lower() == 'y':
                            bet(player, player.chips, game)
                        else:
                            continue
                player.bet(player, amount_bet, game)
                break

            elif action == 'c':
                player.check()
                break

    elif game.current_bet > 0:
    # Player can call, raise, fold, or go all-in
        while True:
            action = input(f"{player.name}, do you want to call, raise, fold, or go all-in? (c/r/f/a): ").strip().lower()
            if action == 'f':
                player.fold()
                break
            elif action == 'c':
                if player.chips >= game.current_bet:
                    bet(player, game.current_bet, game)
                else:
                    print(f"{player.name} does not have enough chips to call {game.current_bet}. Do you want to go all in? (y/n):")
                    if input().strip().lower() == 'y':
                        bet(player,player.chips,game)
                    else:
                        player.fold()
                
            elif action == 'r':
                amount_raise = input(f"{player.name}, enter the amount to raise: ")
                if amount_raise.isdigit():
                    amount_raise = int(amount_raise)
                    if amount_raise > 0 and amount_raise <= player.chips:
                        bet(player, game.current_bet + amount_raise, game)
                    elif amount_raise <= 0:
                        print("Raise amount must be greater than 0.")
                    elif amount_raise > player.chips:
                        print(f"{player.name} does not have enough chips to raise {amount_raise}. Do you want to go all in? (y/n)")
                        if input().strip().lower() == 'y':
                            bet(player, player.chips, game)
                        else:
                            continue
                break
            elif action == 'a':
                bet(player, player.chips, game)
                break
    pass

import Class_poker as poker

p1 = poker.Player("Player 1") 
p2 = poker.Player("Player 2")
game = poker.Game(player1=p1,player2=p2)


def deal(player1,player2,game):
    for _ in range(2):  # Deal two cards to each player
        player1.hand.dealt_card(game.deck.cards.pop())
        player2.hand.dealt_card(game.deck.cards.pop())
    game.state = "pre_flop"

def flop(player1,player2,game):
    for _ in range(3):
        game.dealer_hand.dealt_card(game.deck.cards.pop())
    game.state = "flop"

def turn(player1,player2,game):
    game.dealer_hand.dealt_card(game.deck.cards.pop())
    game.state = "turn"

def river(player1,player2,game):
        game.dealer_hand.dealt_card(game.deck.cards.pop())
        game.state = "river"

def play(player1, player2, game):
    deal(player1, player2, game)
    flop(player1, player2, game)
    turn(player1,player2,game)
    river(player1,player2,game)
    #print(game)

play(p1,p2,game)
print("\n")
poker.evaluate_hand(game,p1)
print("\n")
poker.evaluate_hand(game,p2)
print("\n")
poker.compare_players(p1, p2)


