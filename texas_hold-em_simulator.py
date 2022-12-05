import random
import time


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


def seek_best(cards_):
    # Straight flush 검사
    suit_highest, i = sorted(cards_, key=lambda card_: (card_.suit, Card.ranks[card_.rank][-1]), reverse=True), 0
    while Card.ranks[suit_highest[i].rank][-1] > Card.ranks['5'][-1] and i <= 2:
        for j in range(i + 1, i + 5):
            if suit_highest[j].suit != suit_highest[j - 1].suit or Card.ranks[suit_highest[j].rank][-1] != \
                    Card.ranks[suit_highest[j - 1].rank][-1] - 1:
                i = j
                break
        else:
            return 'Straight flush', suit_highest[i:i + 5]
    suit_lowest, i = sorted(cards_, key=lambda card_: (card_.suit, Card.ranks[card_.rank][0]), reverse=True), 0
    while Card.ranks[suit_lowest[i].rank][0] <= Card.ranks['5'][0] and i <= 2:
        for j in range(i + 1, i + 5):
            if suit_lowest[j].suit != suit_lowest[j - 1].suit or Card.ranks[suit_lowest[j].rank][0] != \
                    Card.ranks[suit_lowest[j - 1].rank][0] - 1:
                i = j
                break
        else:
            return 'Straight flush', suit_lowest[i:i + 5]

    # Four of a kind 검사
    i, highest_suit = 0, sorted(cards_, key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)
    while i <= 3:
        for j in range(i + 1, i + 4):
            if highest_suit[j].rank != highest_suit[j - 1].rank:
                i = j
                break
        else:
            return 'Four of a kind', highest_suit[i:i + 4] + [(highest_suit[:i] + highest_suit[i + 4:])[0]]

    # Full house 검사
    rest, hand_ = highest_suit, []
    for length in (3, 2):
        i = 0
        while i <= len(rest) - length:
            for j in range(i + 1, i + length):
                if rest[j].rank != rest[j - 1].rank:
                    i = j
                    break
            else:
                rest, hand_ = rest[:i] + rest[i + length:], hand_ + rest[i:i + length]
                break
        else:
            break
    else:
        return 'Full house', hand_

    # deque를 이용한 Full house 검사

    return None, None


while True:
    deck = []
    for rank in Card.ranks:
        for suit in Card.suits:
            deck.append(Card(rank, suit))
    random.shuffle(deck)
    players = 2
    holes = tuple([deck.pop() for _ in range(2)] for _ in range(players))
    deck.pop()
    community = [deck.pop() for _ in range(3)]
    for _ in range(2):
        deck.pop()
        community.append(deck.pop())
    for hole in holes:
        cards = hole + community
        t = time.perf_counter_ns()
        name, hand = seek_best(cards)
        if name:
            print(time.perf_counter_ns() - t)
            print(name, hand, cards)
            break
    else:
        continue
    break
