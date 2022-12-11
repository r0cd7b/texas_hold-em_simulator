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
    hand_ = []
    for i, card in enumerate(a_high):
        rank_card = Card.ranks[card.rank][-1]
        if len(hand_) == 0:
            if rank_card > Card.ranks['5'][-1]:
                hand_.append(card)
            else:
                break
        else:
            first = hand_[0]
            comparison = Card.ranks[first.rank][-1] - rank_card - len(hand_)
            if comparison == 0 and first.suit == card.suit:
                hand_.append(card)
                if len(hand_) == 5:
                    return 'Straight flush', hand_
            elif comparison > 0:
                hand_.clear()
        if len(a_high) - (i + 1) < 5 - len(hand_):
            break

    # Lowest Straight flush
    a_low = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][0], reverse=True)
    hand_.clear()
    for i, card in enumerate(a_low):
        rank_card = Card.ranks[card.rank][0]
        if len(hand_) == 0:
            if rank_card == Card.ranks['5'][-1]:
                hand_.append(card)
            else:
                break
        else:
            first = hand_[0]
            comparison = Card.ranks[first.rank][-1] - rank_card - len(hand_)
            if comparison == 0 and first.suit == card.suit:
                hand_.append(card)
                if len(hand_) == 5:
                    return 'Straight flush', hand_
            elif comparison > 0:
                hand_.clear()
        if len(a_low) - (i + 1) < 5 - len(hand_):
            break

    # Four of a kind
    i = 0
    hand_.clear()
    for j in range(1, len(a_high)):
        next_ = j + 1
        if Card.ranks[a_high[i].rank][-1] == Card.ranks[a_high[j].rank][-1]:
            if i + 4 == next_:
                hand_ = a_high[i:next_]
                if i == 0:
                    hand_.append(a_high[next_])
                else:
                    hand_.append(a_high[0])
                return 'Four of a kind', hand_
        else:
            i = j
        if len(a_high) - next_ < 4 - len(hand_):
            break

    # Full house


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
for _ in range(10000):
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
