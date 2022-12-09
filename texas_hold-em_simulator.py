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
    high = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][0], reverse=True)
    hand_ = None
    for card in high:
        rank_card = Card.ranks[card.rank][0]
        if hand_ is None:
            if rank_card > Card.ranks['5'][-1]:
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

    # Lowest Straight flush
    low = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][0], reverse=True)
    hand_ = None
    for card in low:
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

    # Four of a kind
    i, highest_suit = 0, sorted(cards_, key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)
    for j in range(i + 1, len(highest_suit)):
        if highest_suit[i].rank != highest_suit[j].rank:
            if j > len(cards_) - 4:
                break
            i = j
        elif j + 1 - i == 4:
            rest = highest_suit[:i]
            rest.extend(rest[j + 1:j + 2])
            hand_ = highest_suit[i:j + 1]
            hand_.append(rest[0])
            return 'Four of a kind', hand_

    # Full house
    i = 0
    hand_ = []
    rest = sorted(cards_, key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)
    while i <= len(rest) - 3:
        last = i + 3
        for j in range(i + 1, last):
            if rest[j - 1].rank != rest[j].rank:
                i = j
                break
        else:
            i = 0
            hand_.extend(rest[i:last])
            rest = rest[:i] + rest[last:]
            while i <= len(rest) - 2:
                last = i + 2
                for j in range(i + 1, last):
                    if rest[j - 1].rank != rest[j].rank:
                        i = j
                        break
                else:
                    hand_.extend(rest[i:last])
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
    rest, hand_ = highest_suit.copy(), []
    for length in (3, 1, 1):
        i = 0
        while i <= len(rest) - length:
            last = i + length
            for j in range(i + 1, last):
                if rest[i].rank != rest[j].rank:
                    i = j
                    break
            else:
                hand_.extend(rest[i:last])
                del rest[i:last]
                break
        else:
            break
    else:
        return 'Three of a kind', hand_

    # Two pairs
    rest, hand_ = highest_suit.copy(), []
    for length in (2, 2, 1):
        i = 0
        while i <= len(rest) - length:
            last = i + length
            for j in range(i + 1, last):
                if rest[i].rank != rest[j].rank:
                    i = j
                    break
            else:
                hand_.extend(rest[i:last])
                del rest[i:last]
                break
        else:
            break
    else:
        return 'Two pairs', hand_

    # Pair
    rest, hand_ = highest_suit.copy(), []
    for length in (2, 1, 1, 1):
        i = 0
        while i <= len(rest) - length:
            last = i + length
            for j in range(i + 1, last):
                if rest[i].rank != rest[j].rank:
                    i = j
                    break
            else:
                hand_.extend(rest[i:last])
                del rest[i:last]
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

players = 22
counter = Counter()
for _ in range(1000):
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
    print(f'{name}: {count / total * 100:.2f}%')
