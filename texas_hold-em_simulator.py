import random
import time
from collections import deque


class Card:
    """
    ranks = {'2': (1,), '3': (2,), '4': (3,), '5': (4,), '6': (5,), '7': (6,), '8': (7,), '9': (8,), '10': (9,),
             'J': (10,), 'Q': (11,), 'K': (12,), 'A': (0, 13)}
    suits = ('♠', '♣', '♥', '♦')
    """
    ranks = {'2': (1,), '3': (2,), '4': (3,), '5': (4,), '6': (5,), '7': (6,), '8': (7,), '9': (8,), '10': (9,),
             'J': (10,), 'Q': (11,), 'K': (12,), 'A': (0, 13)}
    suits = ('♠', '♣', '♥', '♦')

    def __init__(self, rank_, suit_):
        self.rank = rank_
        self.suit = suit_

    def __repr__(self):
        return self.rank + self.suit


def straight_flush(cards_, i):
    j = 0
    while Card.ranks[cards_[j].rank][i] > Card.ranks['5'][i] and j <= 2:
        for k in range(j, j + 4):
            next_ = k + 1
            if cards_[k].suit != cards_[next_].suit or Card.ranks[cards_[k].rank][i] != \
                    Card.ranks[cards_[next_].rank][i] + 1:
                j = next_
                break
        else:
            return cards_[j:j + 5], 'Straight flush'
    return None


def seek_hand(cards_):
    # Straight flush 검사
    suit_highest, i = sorted(cards_, key=lambda card_: (card_.suit, Card.ranks[card_.rank][-1]), reverse=True), 0
    while Card.ranks[suit_highest[i].rank][-1] > Card.ranks['5'][-1] and i <= 2:
        for k in range(i, i + 4):
            next_ = k + 1
            if suit_highest[k].suit != suit_highest[next_].suit or Card.ranks[suit_highest[k].rank][-1] != \
                    Card.ranks[suit_highest[next_].rank][-1] + 1:
                i = next_
                break
        else:
            return suit_highest[i:i + 5], 'Straight flush'
    suit_lowest, i = sorted(cards_, key=lambda card_: (card_.suit, Card.ranks[card_.rank][-1]), reverse=True), 0
    while Card.ranks[suit_lowest[i].rank][-1] <= Card.ranks['5'][-1] and i <= 2:
        for k in range(i, i + 4):
            next_ = k + 1
            if suit_lowest[k].suit != suit_lowest[next_].suit or Card.ranks[suit_lowest[k].rank][-1] != \
                    Card.ranks[suit_lowest[next_].rank][-1] + 1:
                i = next_
                break
        else:
            return suit_lowest[i:i + 5], 'Straight flush'

    # Four of a kind 검사

    return None, None


while True:
    players = 2

    deck = []
    for rank in Card.ranks:
        for suit in Card.suits:
            deck.append(Card(rank, suit))

    random.shuffle(deck)

    holes = tuple([deck.pop() for _ in range(2)] for _ in range(players))
    deck.pop()
    community = [deck.pop() for _ in range(3)]
    for _ in range(2):
        deck.pop()
        community.append(deck.pop())

    for hole in holes:
        cards = hole + community
        t = time.perf_counter_ns()
        hand, name = seek_hand(cards)
        if name == 'Straight flush':
            print(time.perf_counter_ns() - t)
            print(cards, hand, name)
            break
    else:
        continue
    break
