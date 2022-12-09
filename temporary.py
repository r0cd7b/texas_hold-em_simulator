import random
import time


class Card:
    ranks = {'2': (1,), '3': (2,), '4': (3,), '5': (4,), '6': (5,), '7': (6,), '8': (7,), '9': (8,), '10': (9,),
             'J': (10,), 'Q': (11,), 'K': (12,), 'A': (0, 13)}
    suits = ('♠', '♣')
    hands = {'High card': 0, 'Pair': 1, 'Two pairs': 2, 'Three of a kind': 3, 'Straight': 4, 'Flush': 5,
             'Full house': 6, 'Four of a kind': 7, 'Straight flush': 8}

    def __init__(self, rank_, suit_):
        self.rank = rank_
        self.suit = suit_

    def __repr__(self):
        return self.rank + self.suit


def seek_best(cards_):
    # 5500
    lowest = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][0], reverse=True)
    hand_ = None
    for card in lowest:
        rank_card = Card.ranks[card.rank][0]
        if hand_ is None:
            if rank_card == Card.ranks['5'][-1]:
                hand_ = [card]
            else:
                break
        else:
            end_hand = hand_[-1]
            rank_hand = Card.ranks[end_hand.rank][0] - 1
            comparison = rank_hand - rank_card
            if comparison == 0 and end_hand.suit == card.suit:
                hand_.append(card)
                if len(hand_) == 5:
                    return 'Straight flush', hand_
            elif comparison > 0:
                hand_ = None

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
