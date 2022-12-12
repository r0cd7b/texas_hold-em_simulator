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
    first = a_high[0]
    rank_five = Card.ranks['5'][-1]
    if Card.ranks[first.rank][-1] > rank_five:
        hand_ = [first]
        for i_ in range(1, len(a_high)):
            current = a_high[i_]
            previous = hand_[-1]
            rank_current = Card.ranks[current.rank][-1]
            compare = rank_current - Card.ranks[previous.rank][-1] + 1
            if compare == 0 and current.suit == previous.suit:
                hand_.append(current)
                if len(hand_) == 5:
                    return 'Straight flush', hand_
            elif compare < 0:
                if rank_current <= rank_five:
                    break
                hand_.clear()
                hand_.append(current)
            if len(a_high) - (i_ + 1) < 5 - len(hand_):
                break

    # Lowest Straight flush
    a_low = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][0], reverse=True)
    first = a_low[0]
    rank_five = Card.ranks['5'][0]
    if Card.ranks[first.rank][0] == rank_five:
        hand_ = [first]
        for i_ in range(1, len(a_low)):
            current = a_low[i_]
            previous = hand_[-1]
            rank_current = Card.ranks[current.rank][0]
            compare = rank_current - Card.ranks[previous.rank][0] + 1
            if compare == 0 and current.suit == previous.suit:
                hand_.append(current)
                if len(hand_) == 5:
                    return 'Straight flush', hand_
            elif compare < 0:
                if rank_current != rank_five:
                    break
                hand_.clear()
                hand_.append(current)
            if len(a_low) - (i_ + 1) < 5 - len(hand_):
                break

    # Four of a kind
    hand_ = [a_high[0]]
    for i_ in range(1, len(a_high)):
        current = a_high[i_]
        j = i_ + 1
        if Card.ranks[current.rank][-1] == Card.ranks[hand_[-1].rank][-1]:
            hand_.append(current)
            if len(hand_) == 4:
                k = i_ - 3
                hand_ = a_high[k:j]
                if k == 0:
                    hand_.append(a_high[j])
                else:
                    hand_.append(a_high[0])
                return 'Four of a kind', hand_
        else:
            hand_.clear()
            hand_.append(current)
        if len(a_high) - j < 4 - len(hand_):
            break

    # Full house
    hand_.clear()
    hand_.append(a_high[0])
    sub_hand = []
    for i_ in range(1, len(a_high)):
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
for i in range(10000):
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
