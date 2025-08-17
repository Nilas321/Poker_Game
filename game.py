#creating the poker game
import Class_poker as poker
#pre_flop
#actions - check (bet,0) , - bet(bet,x) . - raise_to(bet, y > x),call (bet,x-z), fold(give up the money) all_in (bet , chips)
def bet(player, amount, game):
    if amount <= player.chips:
        player.bet_amount += amount
        game.pot += amount
        player.chips -= amount
        game.current_bet = max(game.current_bet,amount)
        print(f"{player.name} has bet {amount} chips. Current pot is now {game.pot} chips.")
    else:
        print(f"{player.name} does not have enough chips to bet {amount}.")
        return

def reset_bets(player1, player2, game,state = "not_preflop"):
    game.current_bet = 0
    player1.bet_amount = 0
    player2.bet_amount = 0
    game.check_count = 0
    
    if state == "preflop":
        player1.is_folded = False
        player2.is_folded = False
        player1.is_call = False
        player2.is_call = False
        player1.is_allin = False
        player2.is_allin = False
        game.check_count = 1

def post_blinds(player1, player2, game, sb=10, bb=20):
    bet(player1, sb, game)   # Player 1 posts small blind
    bet(player2, bb, game)   # Player 2 posts big blind
    game.current_bet = bb    # initial current bet = big blind


def action(player,game):
    if game.current_bet == 0:
        # Player can check,bet or fold
        while True:
            action = input(f"{player.name}, do you want to check, bet, or fold? (c/b/f): ").strip().lower()
            if action == 'f':
                player.is_folded = True
                print(f"{player.name} has folded.")
                return
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
                return

            elif action == 'c':
                game.check_count += 1
                bet(player, 0, game)
                return

    elif game.current_bet > 0:
        
    # Player can call, raise, fold, or go all-in
        while True:
            action = input(f"{player.name}, do you want to call, raise, fold, or go all-in? (c/r/f/a): ").strip().lower()
            if action == 'f':
                player.is_folded = True
                print(f"{player.name} has folded.")
                return
            elif action == 'c':
                player.is_call = True
                if player.chips >= game.current_bet:
                    bet(player, game.current_bet, game)
                    return
                
                else:
                    print(f"{player.name} does not have enough chips to call {game.current_bet}. Do you want to go all in? (y/n):")
                    if input().strip().lower() == 'y':
                        bet(player,player.chips,game)
                        player.is_allin = True
                    else:
                        player.is_folded = True
                        print(f"{player.name} has folded.")
                return
                
            elif action == 'r':
                poker_raise = input(f"{player.name}, enter the amount to raise: ") 
                if poker_raise.isdigit():
                    amount_raise = int(poker_raise) + game.current_bet - player.bet_amount
                    if amount_raise > 0 and amount_raise < player.chips:
                        game.current_bet = int(poker_raise) + game.current_bet
                        bet(player,amount_raise, game)
                    elif amount_raise == player.chips:
                        game.current_bet = int(poker_raise) + game.current_bet
                        bet(player, player.chips, game)
                        player.is_allin = True
                        print(f"{player.name} has gone all-in with {player.chips} chips.")
                        return
                    elif amount_raise <= 0:
                        print("Raise amount must be greater than 0.")
                    elif amount_raise > player.chips:
                        print(f"{player.name} does not have enough chips to raise {amount_raise}. Do you want to go all in? (y/n)")
                        if input().strip().lower() == 'y':
                            bet(player, player.chips, game)
                            player.is_allin = True
                        else:
                            continue
                return
            elif action == 'a':
                bet(player, player.chips, game)
                print(f"{player.name} has gone all-in with {player.chips} chips.")
                player.is_allin = True
                return
    return

def game_loop(player1, player2, game,state = "not_preflop"):
    reset_bets(player1, player2, game,state)
    print(f"\nCurrent pot: {game.pot} chips")
    while game.check_count < 2:
        for player in [player1, player2]:
            if not player.is_folded and not player.is_allin and game.check_count < 2:
                action(player, game)
                if player.is_folded or player.is_allin:
                    break
        # break condition: all active players have matched game.current_bet
        if (player1.is_folded or player1.bet_amount == game.current_bet) and (player2.is_folded or player2.bet_amount == game.current_bet):
            break

    player1.is_call = False
    player2.is_call = False
    if player1.is_folded:
        print(f"{player1.name} has folded. {player2.name} wins the pot!")
        player2.chips += game.pot
        return
    elif player2.is_folded:
        print(f"{player2.name} has folded. {player1.name} wins the pot!")
        player1.chips += game.pot
        return
    if player1.is_allin:
        print(f"{player1.name} has gone all-in with {player1.bet_amount} chips.")
        if not player2.is_allin:
            x = input(f"{player2.name}, choose to call or fold(c/f)...")
            if x == 'c':
                if player2.chips >= game.current_bet:
                    bet(player2, game.current_bet, game)
                else:
                    print(f"{player2.name} does not have enough chips to call {game.current_bet}. Do you want to go all in? (y/n):")
                    if input().strip().lower() == 'y':
                        bet(player2,player2.chips,game)
                        player2.is_allin = True
                    else:
                        player2.is_folded = True
                        print(f"{player2.name} has folded.")
                return
            elif x == 'f':
                player2.is_folded = True
                print(f"{player2.name} has folded. {player1.name} wins the pot!")
                player1.chips += game.pot
                return
    elif player2.is_allin:
        print(f"{player2.name} has gone all-in with {player2.bet_amount} chips.")
        if not player1.is_allin:
            x = input(f"{player1.name}, choose to call or fold(c/f)...")
            if x == 'c':
                if player1.chips >= game.current_bet:
                    bet(player1, game.current_bet, game)
                else:
                    print(f"{player1.name} does not have enough chips to call {game.current_bet}. Do you want to go all in? (y/n):")
                    if input().strip().lower() == 'y':
                        bet(player1,player1.chips,game)
                        player1.is_allin = True
                    else:
                        player1.is_folded = True
                        print(f"{player1.name} has folded.")
                return
            elif x == 'f':
                player1.is_folded = True
                print(f"{player1.name} has folded. {player2.name} wins the pot!")
                player2.chips += game.pot
    return

def state_check(player1, player2):
    if player1.is_folded or player2.is_folded:
        print("Game ended due to a fold.")
        return "end"
    elif player1.is_allin or player2.is_allin:
        print("A player went all-in. Continuing to the next round.")
        return "allcontinue"
    else:
        print("Both players have checked or called. Continuing to the next round.")
        return "continue"


p1 = poker.Player("Player 1") 
p2 = poker.Player("Player 2")
game = poker.Game(player1=p1,player2=p2)


def deal(player1,player2,game):
    for _ in range(2):  # Deal two cards to each player
        player1.hand.dealt_card(game.deck.cards.pop())
        player2.hand.dealt_card(game.deck.cards.pop())
    print(f"{player1.name} has been dealt: {player1.hand}")
    print(f"{player2.name} has been dealt: {player2.hand}")
    
    bet(player1,20,game)
    bet(player2,10,game)

    while True:
        action = input(f"{player2.name}, do you want to call, raise, fold, or go all-in? (c/r/f/a): ").strip().lower()
        if action == 'f':
            player2.is_folded = True
            print(f"{player2.name} has folded.")
            player1.chips += game.pot
            game.state = "end"
            return
        elif action == 'c':
            if player2.chips >= game.current_bet - player2.bet_amount:
                bet(player2, game.current_bet - player2.bet_amount, game)
                break
            
            else:
                print(f"{player2.name} does not have enough chips to call {game.current_bet}. Do you want to go all in? (y/n):")
                if input().strip().lower() == 'y':
                    bet(player2,player2.chips,game)
                    player2.is_allin = True
                else:
                    player2.is_folded = True
                    print(f"{player2.name} has folded.")
                    player1.chips += game.pot
                    game.state = "end"
                    return
            break
            
        elif action == 'r':
            poker_raise = input(f"{player2.name}, enter the amount to raise: ") 
            if poker_raise.isdigit():
                amount_raise = int(poker_raise) + game.current_bet - player2.bet_amount
                if amount_raise > 0 and amount_raise < player2.chips:
                    game.current_bet = int(poker_raise) + game.current_bet
                    bet(player2,amount_raise, game)
                elif amount_raise == player2.chips:
                    game.current_bet = int(poker_raise) + game.current_bet
                    bet(player2, player2.chips, game)
                    player2.is_allin = True
                    print(f"{player2.name} has gone all-in with {player2.chips} chips.")
                    break
                elif amount_raise <= 0:
                    print("Raise amount must be greater than 0.")
                elif amount_raise > player2.chips:
                    print(f"{player2.name} does not have enough chips to raise {amount_raise}. Do you want to go all in? (y/n)")
                    if input().strip().lower() == 'y':
                        bet(player2, player2.chips, game)
                        player2.is_allin = True
                    else:
                        continue
            break
        elif action == 'a':
            bet(player2, player2.chips, game)
            print(f"{player2.name} has gone all-in with {player2.chips} chips.") 
            player2.is_allin = True
            break

    if game.state == "continue":
        game_loop(player1, player2, game,state = "preflop")
    game.state = state_check(player1, player2)
    return

def flop(player1,player2,game):
    for _ in range(3):
        game.dealer_hand.dealt_card(game.deck.cards.pop())
    print(f"Dealer's hand: {game.dealer_hand}")
    if game.state == "continue":
        game_loop(player1, player2, game)
    
    game.state = state_check(player1, player2)
    return

def turn(player1,player2,game):
    game.dealer_hand.dealt_card(game.deck.cards.pop())
    print(f"Dealer's hand: {game.dealer_hand}")
    if game.state == "continue":
        game_loop(player1, player2, game)
    game.state = state_check(player1, player2)
    return

def river(player1,player2,game):
    game.dealer_hand.dealt_card(game.deck.cards.pop())
    print(f"Dealer's hand: {game.dealer_hand}")
    if game.state == "continue":
        game_loop(player1, player2, game)
    game.state = state_check(player1, player2)

def play(player1, player2, game):
    print("Starting the game...")
    game.deck.shuffle()  # Shuffle the deck before dealing cards
    deal(player1, player2, game)
    if game.state == "end":
        return
    flop(player1, player2, game)
    if game.state == "end":
        return
    turn(player1,player2,game)
    if game.state == "end":
        return
    river(player1,player2,game)
    if game.state == "end":
        return
    #print(game)

play(p1,p2,game)


if not game.state == "end":
    print("\n")
    poker.evaluate_hand(game,p1)
    print("\n")
    poker.evaluate_hand(game,p2)
    print("\n")
    poker.compare_players(p1, p2,game)

    print(f"\n p1 chips: {p1.chips} ,p2 chips: {p2.chips}")
else:
    print(f"\n p1 chips: {p1.chips} ,p2 chips: {p2.chips}")

