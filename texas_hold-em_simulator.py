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
    a_high = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][-1], reverse=True)
    if Card.ranks[a_high[0].rank][-1] > Card.ranks['5'][-1]:
        hand_ = [a_high[0]]
        for i in range(1, len(cards_)):
            if Card.ranks[a_high[i].rank][-1] == Card.ranks[hand_[-1].rank][-1] - 1 and a_high[i].suit == \
                    hand_[-1].suit:
                hand_.append(a_high[i])
                if len(hand_) == 5:
                    return 'Straight flush', hand_
            elif Card.ranks[a_high[i].rank][-1] < Card.ranks[hand_[-1].rank][-1] - 1:
                if Card.ranks[a_high[i].rank][-1] <= Card.ranks['5'][-1]:
                    break
                hand_ = [a_high[i]]
            if len(cards_) - (i + 1) < 5 - len(hand_):
                break

    # Lowest Straight flush
    a_low = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][0], reverse=True)
    if Card.ranks[a_low[0].rank][0] == Card.ranks['5'][0]:
        hand_ = [a_low[0]]
        for i in range(1, len(cards_)):
            if Card.ranks[a_low[i].rank][0] == Card.ranks[hand_[-1].rank][0] - 1 and a_high[i].suit == hand_[-1].suit:
                hand_.append(a_low[i])
                if len(hand_) == 5:
                    return 'Straight flush', hand_
            elif Card.ranks[a_low[i].rank][0] < Card.ranks[hand_[-1].rank][0] - 1:
                if Card.ranks[a_low[i].rank][0] != Card.ranks['5'][0]:
                    break
                hand_ = [a_low[i]]
            if len(cards_) - (i + 1) < 5 - len(hand_):
                break

    # Four of a kind
    hand_ = [a_high[0]]
    for i in range(1, len(cards_)):
        if Card.ranks[a_high[i].rank][-1] == Card.ranks[hand_[-1].rank][-1]:
            hand_.append(a_high[i])
            if len(hand_) == 4:
                return 'Four of a kind', hand_ + (a_high[:i - 3] + a_high[i + 1:i + 2])[:1]
        else:
            hand_ = [a_high[i]]
        if len(cards_) - (i + 1) < 5 - len(hand_):
            break

    # Full house
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

    # Flush
    suit_higher = sorted(cards_, key=lambda card_: (card_.suit, Card.ranks[card_.rank][-1]), reverse=True)
    k = 0
    for m in range(1, len(cards_)):
        if suit_higher[k].suit == suit_higher[m].suit:
            next_m = m + 1
            if next_m - k == 5:
                return 'Flush', suit_higher[k:next_m]
        else:
            if len(cards_) - m < 5:
                break
            k = m

    # High Straight

    # Lowest Straight

    # Three of a kind

    # Two pairs

    # Pair

    # High card
    return 'High card', a_high[:5]


deck = []
for rank in Card.ranks:
    for suit in Card.suits:
        deck.append(Card(rank, suit))

players = 22
counter = Counter()
for _ in range(40000):
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
