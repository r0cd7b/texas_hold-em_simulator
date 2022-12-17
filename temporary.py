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
    length_cards = len(cards_)
    hand_ = [a_high[0]]
    breakpoint_ = length_cards - 5
    pair_later = False
    for i in range(1, length_cards):
        length_hand = len(hand_)
        if i - length_hand > breakpoint_:
            break
        card = a_high[i]
        if Card.ranks[card.rank][-1] == Card.ranks[hand_[-1].rank][-1]:
            hand_.append(card)
            length_hand = len(hand_)
            if length_hand >= 5:
                if pair_later:
                    return 'Full house', hand_
                return 'Full house', hand_[2:] + hand_[:2]
            if length_hand == 3:
                pair_later = True
        elif length_hand > 3:
            if pair_later:
                hand_[3] = card
            else:
                hand_[2] = card
                hand_.pop()
        elif length_hand == 3:
            if pair_later:
                hand_.append(card)
            else:
                hand_[2] = card
        elif length_hand >= 2:
            hand_.append(card)
        else:
            hand_ = [card]

    return None, None


seed = 15
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
