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
        for i_ in range(1, len(cards_)):
            if Card.ranks[a_high[i_].rank][-1] == Card.ranks[hand_[-1].rank][-1] - 1 and a_high[i_].suit == \
                    hand_[-1].suit:
                hand_.append(a_high[i_])
                if len(hand_) == 5:
                    return 'Straight flush', hand_
            elif Card.ranks[a_high[i_].rank][-1] < Card.ranks[hand_[-1].rank][-1] - 1:
                if Card.ranks[a_high[i_].rank][-1] <= Card.ranks['5'][-1]:
                    break
                hand_ = [a_high[i_]]
            if len(cards_) - (i_ + 1) < 5 - len(hand_):
                break

    # Lowest Straight flush
    a_low = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][0], reverse=True)
    if Card.ranks[a_low[0].rank][0] > Card.ranks['5'][0]:
        hand_ = [a_low[0]]
        for i_ in range(1, len(cards_)):
            if Card.ranks[a_low[i_].rank][0] == Card.ranks[hand_[-1].rank][0] - 1 and a_high[i_].suit == hand_[-1].suit:
                hand_.append(a_low[i_])
                if len(hand_) == 5:
                    return 'Straight flush', hand_
            elif Card.ranks[a_low[i_].rank][0] < Card.ranks[hand_[-1].rank][0] - 1:
                if Card.ranks[a_low[i_].rank][0] <= Card.ranks['5'][0]:
                    break
                hand_ = [a_low[i_]]
            if len(cards_) - (i_ + 1) < 5 - len(hand_):
                break

    # Four of a kind
    hand_ = [a_high[0]]
    for i_ in range(1, len(cards_)):
        if Card.ranks[a_high[i_].rank][-1] == Card.ranks[hand_[-1].rank][-1]:
            hand_.append(a_high[i_])
            if len(hand_) == 4:
                return 'Four of a kind', hand_ + (a_high[:i_ - 3] + a_high[i_ + 1:i_ + 2])[:1]
        else:
            hand_ = [a_high[0]]
        if len(cards_) - (i_ + 1) < 4 - len(hand_):
            break

    # Full house
    hand_, sub_hand = [a_high[0]], []
    for i_ in range(1, len(cards_)):
        if Card.ranks[a_high[i_].rank][-1] == Card.ranks[hand_[-1].rank][-1]:
            hand_.append(a_high[i_])
            if len(hand_) == 5:
                return 'Full house', hand_
            if len(hand_) == 3 and len(sub_hand) == 2:
                return 'Full house', hand_ + sub_hand
        else:
            if len(hand_) in (4, 1):
                hand_.pop()
            elif len(hand_) == 2:
                if len(sub_hand) == 0:
                    sub_hand = [card for card in hand_]
                hand_.clear()
            hand_.append(a_high[i_])
        if len(cards_) - (i_ + 1) < 5 - (len(hand_) + len(sub_hand)):
            break

    # Flush

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
for i in range(50000):
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
    print(f'{name}: {count / total * 100:.4f}%')
