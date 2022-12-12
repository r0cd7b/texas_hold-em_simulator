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
    first = a_high[0]
    length_cards = len(cards_)
    hand_ = [first]

    print(a_high)
    hand_.clear()
    hand_.append(first)
    sub_hand = []
    for i_ in range(1, length_cards):
        current = a_high[i_]
        length_sub = len(sub_hand)
        if Card.ranks[current.rank][-1] == Card.ranks[hand_[-1].rank][-1]:
            hand_.append(current)
            length_hand = len(hand_)
            if length_hand == 5:
                return 'Full house', hand_
            if length_hand == 3 and length_sub == 2:
                hand_.extend(sub_hand)
                return 'Full house', hand_
        else:
            length_hand = len(hand_)
            if length_hand in (4, 1):
                hand_.pop()
            elif length_hand == 2:
                if length_sub == 0:
                    for card in hand_:
                        sub_hand.append(card)
                hand_.clear()
            hand_.append(current)
        if length_cards - (i_ + 1) < 5 - (len(hand_) + len(sub_hand)):
            break

    return None, None


i = 144
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
        if name == 'Full house':
            print(i, name, hand, cards)
            break
    else:
        i += 1
        continue
    break
