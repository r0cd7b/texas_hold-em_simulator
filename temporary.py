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
    a_high = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][-1], reverse=True)
    print(a_high)

    hand_ = [a_high[0]]
    for i_ in range(1, len(a_high)):
        current = a_high[i_]
        j = i_ + 1
        if Card.ranks[current.rank][-1] == Card.ranks[hand_[-1].rank][-1]:
            hand_.append(current)
            if len(hand_) == 4:
                k = i_ - 3
                hand_ = a_high[k:j]
                if k == 0:
                    hand_.append(a_high[j])
                else:
                    hand_.append(a_high[0])
                return 'Four of a kind', hand_
        else:
            hand_.clear()
            hand_.append(current)
        if len(a_high) - j < 4 - len(hand_):
            break

    return None, None


i = 0
while True:
    deck = []
    for rank in Card.ranks:
        for suit in Card.suits:
            deck.append(Card(rank, suit))

    random.seed(i)
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
        if name == 'Four of a kind':
            print(i, name, hand, cards)
            break
    else:
        i += 1
        continue
    break
