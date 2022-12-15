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
    def f1():
        sorted(cards_, key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)

    def f2():
        sorted(cards_, key=lambda card_: Card.ranks[card_.rank][-1], reverse=True)

    print(timeit.timeit(f1))
    print(timeit.timeit(f2))
    print()

    a_high_suit = sorted(cards_, key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)
    hand_ = []
    breakpoint_ = len(cards_) - 5
    for i, card in enumerate(a_high_suit):
        if i - len(hand_) > breakpoint_:
            break
        if not hand_:
            hand_.append(card)
        elif card.suit != hand_[-1].suit:
            hand_ = [card]
        else:
            hand_.append(card)
            if len(hand_) == 5:
                return 'Flush', hand_

    return None, None


seed = 0
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
