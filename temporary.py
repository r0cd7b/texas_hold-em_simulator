import random
import time
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
    a_high = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][-1], reverse=True)
    hand_ = []

    # def f1():
    #
    # def f2():
    #
    # print(timeit.timeit(f1))
    # print(timeit.timeit(f2))

    length, i = len(a_high), 0
    for j in range(1, length):
        next_ = j + 1
        if Card.ranks[a_high[i].rank][-1] == Card.ranks[a_high[j].rank][-1]:
            if i + 4 == next_:
                hand_ = a_high[i:next_]
                if i == 0:
                    hand_.append(a_high[next_])
                else:
                    hand_.append(a_high[0])
                return 'Four of a kind', hand_
        else:
            i = j
        if length - next_ < 4 - len(hand_):
            break

    return None, None


deck = []
for rank in Card.ranks:
    for suit in Card.suits:
        deck.append(Card(rank, suit))

name = None
while True:
    random.shuffle(deck)

    holes = tuple([deck.pop() for _ in range(2)] for _ in range(1))
    burn = [deck.pop()]
    community = [deck.pop() for _ in range(3)]
    for _ in range(2):
        burn.append(deck.pop())
        community.append(deck.pop())

    for hole in holes:
        cards = hole + community
        t = time.perf_counter_ns()
        name, hand = seek_best(cards)
        if name:
            print(time.perf_counter_ns() - t)
            print(name, hand, cards)
            break
    if name:
        break

    for hole in holes:
        while hole:
            deck.append(hole.pop())
    while burn:
        deck.append(burn.pop())
    while community:
        deck.append(community.pop())
