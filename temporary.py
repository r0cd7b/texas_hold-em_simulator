import random
import timeit


class Card:
    ranks = {'2': (1,), '3': (2,), '4': (3,), '5': (4,), '6': (5,), '7': (6,), '8': (7,), '9': (8,), '10': (9,),
             'J': (10,), 'Q': (11,), 'K': (12,), 'A': (0, 13)}
    suits = ('♠', '♣', '♥', '♦')

    def __init__(self, rank_, suit_):
        self.rank = rank_
        self.suit = suit_

    def __repr__(self):
        return self.rank + self.suit


def seek_best(cards_):
    # def f1():
    #
    # def f2():
    #
    # print(timeit.timeit(f1))
    # print(timeit.timeit(f2))
    # print()

    a_high = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][-1], reverse=True)
    cards_check = a_high.copy()
    hand_ = []
    for length_combinations in (3, 2):
        length_check = len(cards_check)
        sub_hand = [cards_check[0]]
        breakpoint_ = length_check - length_combinations
        cards_rest = []
        for i in range(1, length_check):
            if i - len(sub_hand) > breakpoint_:
                break
            card = cards_check[i]
            if len(sub_hand) >= length_combinations:
                cards_rest.append(card)
            elif card.suit == sub_hand[-1].suit:
                sub_hand.append(card)
            else:
                sub_hand = [card]
        else:
            cards_check = cards_rest
            hand_.extend(sub_hand)
            continue
        break

    return None, None


seed = 18
while True:
    deck = []
    for rank in Card.ranks:
        for suit in Card.suits:
            deck.append(Card(rank, suit))

    random.seed(seed)
    random.shuffle(deck)

    holes = tuple([deck.pop() for _ in range(2)] for _ in range(1))
    burn = [deck.pop()]
    community = [deck.pop() for _ in range(3)]
    for _ in range(2):
        burn.append(deck.pop())
        community.append(deck.pop())

    for hole in holes:
        cards = hole + community
        name, hand = seek_best(cards)
        if name:
            print(seed, name, hand, cards)
            break
    else:
        seed += 1
        continue
    break
