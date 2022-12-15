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
    cards = a_high.copy()
    cards = []
    for length in (3, 2):
        sub_hand = []
        breakpoint_ = len(a_high) - 5
        for i, card in enumerate(a_high):
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

    hand_1, hand_2 = [], []
    for i, card in enumerate(a_high):
        if i - len(hand_1) - len(hand_2) > breakpoint_:
            break
        if not hand_1:
            hand_1.append(card)
        else:
            if Card.ranks[card.rank][-1] != Card.ranks[hand_1[-1].rank][-1]:
                if len(hand_1) == 1:
                    hand_1 = [card]
                elif len(hand_1) == 2:
                    if hand_2:
                        hand_1 = [card]
                    else:
                        hand_2 = hand_1
                        hand_1 = []
                elif len(hand_1) == 3:

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
