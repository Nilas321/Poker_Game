from itertools import combinations

RANKS = "23456789TJQKA"
SUITS = "cdhs"                        # clubs, diamonds, hearts, spades
RANK_VAL = {r: i for i, r in enumerate(RANKS, start=2)}

def is_straight(vals):
    """Return top‐card of a straight or None."""
    vals = sorted(set(vals), reverse=True)
    for i in range(len(vals) - 4):
        if vals[i] - vals[i + 4] == 4:
            return vals[i]
    # Wheel A-5 straight
    return 5 if {14, 5, 4, 3, 2}.issubset(vals) else None

def hand_rank(cards):
    """Return sortable rank tuple for a 5-card hand."""
    vals = sorted((RANK_VAL[c[0]] for c in cards), reverse=True)
    suits = [c[1] for c in cards]

    # Flush?
    flush = max((suits.count(s), s) for s in SUITS)[0] == 5
    # Straight?
    straight_top = is_straight(vals)

    if flush and straight_top:
        return (8, straight_top)                   # Straight flush
    counts = sorted(((vals.count(v), v) for v in set(vals)), reverse=True)
    (c1, v1), (c2, v2), *rest = counts + [(0, 0), (0, 0)]
    if c1 == 4:   return (7, v1, rest[0][1])       # Four of a kind
    if c1 == 3 and c2 == 2: return (6, v1, v2)     # Full house
    if flush:     return (5, vals)                 # Flush
    if straight_top: return (4, straight_top)      # Straight
    if c1 == 3:   return (3, v1, sorted(rest + [(v2,)], reverse=True)) # Trips
    if c1 == c2 == 2:
        kick = max(rest[0][1], rest[1][1])
        return (2, max(v1, v2), min(v1, v2), kick) # Two pair
    if c1 == 2:   return (1, v1, sorted(v for v in vals if v != v1))   # One pair
    return (0, vals)                               # High card

def best_five_of_seven(seven):
    """Return best 5-card hand (tuple of cards) and its rank tuple."""
    best = None
    for comb in combinations(seven, 5):
        rank = hand_rank(comb)
        if best is None or rank > best[1]:
            best = (comb, rank)
    return best

def showdown(p1, p2):
    best1, rank1 = best_five_of_seven(p1)
    best2, rank2 = best_five_of_seven(p2)
    if rank1 > rank2:    winner = "Player 1"
    elif rank2 > rank1:  winner = "Player 2"
    else:
        c1 = sorted((RANK_VAL[c[0]] for c in p1), reverse=True)   
        c2 = sorted((RANK_VAL[c[0]] for c in p2), reverse=True)     
        if c1>c2:
            winner='Player 1'
        if c1<c2:
            winner='Player 2'          
        if c1==c2:
            winner='Tie'
    return best1, best2, winner

# --- demo ----------------------------------------------------------
if __name__ == "__main__":
    player1 = ["9c","9d","9h","9s","2h","Td","2c"]   # royal flush
    player2 = ["9c","9d","9h","9s","5d","3h","4c"]   # quads
    b1, b2, who = showdown(player1, player2)
    print("P1 best:", b1, "\nP2 best:", b2, "\nWinner:", who)
