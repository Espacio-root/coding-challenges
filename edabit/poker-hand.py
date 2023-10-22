def poker_hand_ranking(hand):
    suits = [s[-1] for s in hand]
    values = [s[:-1] for s in hand]
    s_cts = [1 if s in values else 0 for s in 'A2345678910JQK']
    s_cts = False if True in [s_cts[i-1] == s_cts[i+1] != s_cts[i] for i in range(1,len(s_cts)-1)] else True
    print(s_cts)
    v_cts = [values.count(v) for v in set(values)]
    
    if len(set(suits)) == 1:
        if not [v for v in values if not v.isalpha() and v != '10']:
            return 'Royal Flush'
        elif s_cts:
            return 'Straight Flush'
        else:
            return 'Flush'

    elif 4 in v_cts:
        return 'Four of a Kind'
    elif 3 in v_cts and 2 in v_cts:
        return 'Full House'
    elif 3 in v_cts:
        return 'Three of a Kind'
    elif v_cts.count(2) == 2:
        return 'Two Pair'
    elif 2 in v_cts:
        return 'Pair'

    elif s_cts:
        return 'Straight'
    
    else:
        return 'High Card'

# Elegant

def poker_hand_ranking(deck):
    order = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    ranks = sorted([i[:-1] for i in deck], key=order.index)
    flush = len(set(i[-1] for i in deck)) == 1
    group = tuple(sorted([ranks.count(r) for r in set(ranks)], reverse=True))
    straight = len(set(ranks)) == 5 and order.index(ranks[-1]) - order.index(ranks[0]) == 4

    if straight and flush:
        return 'Royal Flush' if ranks[-1] == 'A' else 'Straight Flush'
    if straight:
        return 'Straight'
    if flush:
        return 'Flush'

    hands = {(4, 1): 'Four of a Kind', 
             (3, 2): 'Full House', 
             (3, 1, 1): 'Three of a Kind',
             (2, 2, 1): 'Two Pair', 
             (2, 1, 1, 1): 'Pair', 
             (1, 1, 1, 1, 1): 'High Card'}

    return hands[group]


print(poker_hand_ranking(["10s", "9s", "8s", "6s", "7s"]))
