import random
import time


class Card:
    """
    ranks = {'A': (0, 13), '2': (1,), '3': (2,), '4': (3,), '5': (4,), '6': (5,), '7': (6,), '8': (7,), '9': (8,),
             '10': (9,), 'J': (10,), 'Q': (11,), 'K': (12,)}
    suits = {'♠': 0, '♣': 1, '♥': 2, '♦': 3}
    """
    ranks = {'A': (0, 13), '2': (1,), '3': (2,), '4': (3,), '5': (4,), '6': (5,), '7': (6,), '8': (7,), '9': (8,),
             '10': (9,), 'J': (10,), 'Q': (11,), 'K': (12,)}
    suits = {'♠': 0, '♣': 1, '♥': 2, '♦': 3}

    def __init__(self):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return self.rank + self.suit


def seek_best(hand):
    # Straight flush 찾기
    suit_highest = sorted(hand, key=lambda card_: (card_.suit, Card.ranks[card_.rank][-1]), reverse=True)
    stopping = len(hand) - 5

    i_ = 0
    while i_ <= stopping:
        for j in range(i_, i_ + 4):
            if Card.ranks[suit_highest[j].rank][0] != Card.ranks[suit_highest[j + 1].rank][0] + 1 or \
                    suit_highest[j].suit != suit_highest[j + 1].suit:
                i_ = j + 1
                break
        else:
            return suit_highest[i_:i_ + 5], 'Straight flush'

    # Lowest straight flush 찾기
    # suit_lowest = sorted(hand, key=lambda card_: (card_.suit, Card.ranks[card_.rank][0]), reverse=True)
    # starting = -1
    # for i_, card in enumerate(suit_lowest):
    #     if card.rank == '5':
    #         if i_ <= stopping:
    #             starting = i_
    #         else:
    #             break
    #     elif starting >= 0:
    #         if Card.ranks[suit_lowest[i_].rank][0] == Card.ranks[suit_lowest[i_ - 1].rank][0] - 1 and \
    #                 suit_lowest[i_].suit == suit_lowest[i_ - 1].suit:
    #             if i_ + 1 - starting == 5:
    #                 return suit_lowest[starting:i_ + 1], 'Straight flush'
    #         else:
    #             starting = -1

    # Four of a kind 찾기
    highest_suit = sorted(hand, key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)

    return highest_suit[:5], 'High card'


while True:

    players = 2

    cards = []
    for rank in Card.ranks:
        for suit in Card.suits:
            cards.append(Card())

    random.shuffle(cards)

    hands = tuple([cards.pop(), cards.pop()] for _ in range(players))
    cards.pop()
    community = [cards.pop(), cards.pop(), cards.pop()]
    cards.pop()
    community.append(cards.pop())
    cards.pop()
    community.append(cards.pop())

    for i in range(players):
        hands[i].extend(community)
        t = time.perf_counter_ns()
        best, name = seek_best(hands[i])
        if name == 'Straight flush':
            print(time.perf_counter_ns() - t)
            print(name, best, hands[i])

            break
    else:
        continue
    break
