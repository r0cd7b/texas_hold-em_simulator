import random


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
    higher_suit = sorted(cards_, key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)
    i = j = k = 0
    for m in range(1, len(cards_)):
        length_front = j - i
        if Card.ranks[higher_suit[k].rank][-1] == Card.ranks[higher_suit[m].rank][-1]:
            next_m = m + 1
            length_back = next_m - k
            front_part = higher_suit[i:j]
            back_part = higher_suit[k:next_m]
            if length_front > 2:
                if length_back == 2:
                    front_part.extend(back_part)
                    return 'Full house', front_part
            elif length_front == 2:
                if length_back > 2:
                    front_part.extend(back_part)
                    return 'Full house', front_part
        else:
            if length_front < 2:
                length_back = m - k
                if length_back == 2:
                    i = k
                    j = i + 2
                elif length_back > 2:
                    i = k
                    j = i + 3
            if len(cards_) - m < 5 - (j - i):
                break
            k = m

    return None, None


seed = 10
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
