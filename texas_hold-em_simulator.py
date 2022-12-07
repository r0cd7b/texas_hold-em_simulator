from collections import Counter
import random


class Card:
    ranks = {'2': (1,), '3': (2,), '4': (3,), '5': (4,), '6': (5,), '7': (6,), '8': (7,), '9': (8,), '10': (9,),
             'J': (10,), 'Q': (11,), 'K': (12,), 'A': (0, 13)}
    suits = ('♠', '♣', '♥', '♦')
    hands = {'High card': 0, 'Pair': 1, 'Two pairs': 2, 'Three of a kind': 3, 'Straight': 4, 'Flush': 5,
             'Full house': 6, 'Four of a kind': 7, 'Straight flush': 8}

    def __init__(self, rank_, suit_):
        self.rank = rank_
        self.suit = suit_

    def __repr__(self):
        return self.rank + self.suit


def seek_best(cards_):
    # High Straight flush
    suit_highest = sorted(cards_, key=lambda card_: (card_.suit, Card.ranks[card_.rank][-1]), reverse=True)
    i = 0
    while Card.ranks[suit_highest[i].rank][-1] > Card.ranks['5'][-1] and i <= len(cards_) - 5:
        last = i + 5
        for j in range(i + 1, last):
            previous = j - 1
            if Card.ranks[suit_highest[previous].rank][-1] - 1 != Card.ranks[suit_highest[j].rank][-1] or \
                    suit_highest[j].suit != suit_highest[previous].suit:
                i = j
                break
        else:
            return 'Straight flush', suit_highest[i:last]

    # Lowest Straight flush
    suit_lowest = sorted(cards_, key=lambda card_: (card_.suit, Card.ranks[card_.rank][0]), reverse=True)
    i = 0
    while Card.ranks[suit_lowest[i].rank][0] <= Card.ranks['5'][0] and i <= len(cards_) - 5:
        last = i + 5
        for j in range(i + 1, last):
            previous = j - 1
            if Card.ranks[suit_lowest[previous].rank][0] - 1 != Card.ranks[suit_lowest[j].rank][0] or \
                    suit_lowest[j].suit != suit_lowest[previous].suit:
                i = j
                break
        else:
            return 'Straight flush', suit_lowest[i:last]

    # Four of a kind
    highest_suit = sorted(cards_, key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)
    i = 0
    while i <= len(cards_) - 4:
        last = i + 4
        for j in range(i + 1, last):
            if highest_suit[j - 1].rank != highest_suit[j].rank:
                i = j
                break
        else:
            return 'Four of a kind', highest_suit[i:last] + (highest_suit[:i] + highest_suit[last:])[:1]

    # Full house
    check = highest_suit
    hand_ = []
    for length in (3, 2):
        i = 0
        while i <= len(check) - length:
            for j in range(i + 1, i + length):
                if check[j - 1].rank != check[j].rank:
                    i = j
                    break
            else:
                hand_ += check[i:i + length]
                check = check[:i] + check[i + length:]
                break
        else:
            break
    else:
        return 'Full house', hand_

    # Flush
    i = 0
    while i <= len(cards_) - 5:
        last = i + 5
        for j in range(i + 1, last):
            if suit_highest[j - 1].suit != suit_highest[j].suit:
                i = j
                break
        else:
            return 'Flush', suit_highest[i:last]

    # High Straight
    hand_ = [highest_suit[0]]
    i = 1
    while i <= len(cards_) - 5 + len(hand_):
        if Card.ranks[hand_[-1].rank][-1] - 1 == Card.ranks[highest_suit[i].rank][-1]:
            hand_.append(highest_suit[i])
            if len(hand_) == 5:
                return 'Straight', hand_
        else:
            hand_ = [highest_suit[i]]
        i += 1

    # Lowest Straight
    lowest_suit = sorted(cards_, key=lambda card_: (Card.ranks[card_.rank][0], card_.suit), reverse=True)
    hand_ = [lowest_suit[0]]
    i = 1
    while i <= len(cards_) - 5 + len(hand_):
        if Card.ranks[hand_[-1].rank][0] - 1 == Card.ranks[lowest_suit[i].rank][0]:
            hand_.append(lowest_suit[i])
            if len(hand_) == 5:
                return 'Straight', hand_
        else:
            hand_ = [lowest_suit[i]]
        i += 1

    # Three of a kind
    check, hand_ = highest_suit.copy(), []
    for length in (3, 1, 1):
        i = 0
        while i <= len(check) - length:
            last = i + length
            for j in range(i + 1, last):
                if check[i].rank != check[j].rank:
                    i = j
                    break
            else:
                hand_.extend(check[i:last])
                del check[i:last]
                break
        else:
            break
    else:
        return 'Three of a kind', hand_

    # Two pairs
    check, hand_ = highest_suit.copy(), []
    for length in (2, 2, 1):
        i = 0
        while i <= len(check) - length:
            last = i + length
            for j in range(i + 1, last):
                if check[i].rank != check[j].rank:
                    i = j
                    break
            else:
                hand_.extend(check[i:last])
                del check[i:last]
                break
        else:
            break
    else:
        return 'Two pairs', hand_

    # Pair
    check, hand_ = highest_suit.copy(), []
    for length in (2, 1, 1, 1):
        i = 0
        while i <= len(check) - length:
            last = i + length
            for j in range(i + 1, last):
                if check[i].rank != check[j].rank:
                    i = j
                    break
            else:
                hand_.extend(check[i:last])
                del check[i:last]
                break
        else:
            break
    else:
        return 'Pair', hand_

    # High card
    return 'High card', highest_suit[:5]


deck = []
for rank in Card.ranks:
    for suit in Card.suits:
        deck.append(Card(rank, suit))

players = 4

counter = Counter()
for _ in range(100000):
    random.shuffle(deck)

    holes = tuple([deck.pop() for _ in range(2)] for _ in range(players))

    burn = [deck.pop()]
    community = [deck.pop() for _ in range(3)]
    for _ in range(2):
        burn.append(deck.pop())
        community.append(deck.pop())

    for hole in holes:
        cards = hole + community
        name, hand = seek_best(cards)
        counter[name] += 1

    for hole in holes:
        while hole:
            deck.append(hole.pop())
    while burn:
        deck.append(burn.pop())
    while community:
        deck.append(community.pop())

total = counter.total()
for name, count in counter.most_common():
    print(f'{name}: {count / total * 100:.3f}%')
