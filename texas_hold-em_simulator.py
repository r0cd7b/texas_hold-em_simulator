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
    suit_higher = sorted(cards_, key=lambda card_: (card_.suit, Card.ranks[card_.rank][-1]), reverse=True)
    i = 0
    five_rank = Card.ranks['5']
    five = five_rank[-1]
    if Card.ranks[suit_higher[i].rank][-1] > five:
        for j in range(1, len(cards_)):
            first_card = suit_higher[i]
            current_rank = Card.ranks[suit_higher[j].rank][-1]
            current_card = suit_higher[j]
            if Card.ranks[first_card.rank][-1] == current_rank + (j - i) and first_card.suit == current_card.suit:
                next_j = j + 1
                if next_j - i >= 5:
                    return 'Straight flush', suit_higher[i:next_j]
            elif current_rank <= five or len(cards_) - j < 5:
                break
            else:
                i = j

    # Lowest Straight flush
    suit_lower = sorted(cards_, key=lambda card_: (card_.suit, Card.ranks[card_.rank][0]), reverse=True)
    i = 0
    five = five_rank[0]
    if Card.ranks[suit_lower[i].rank][0] == five:
        for j in range(1, len(cards_)):
            current_rank = Card.ranks[suit_lower[j].rank][0]
            if Card.ranks[suit_lower[i].rank][0] == current_rank + (j - i) and suit_lower[i].suit == suit_lower[j].suit:
                next_j = j + 1
                if next_j - i >= 5:
                    return 'Straight flush', suit_lower[i:next_j]
            elif current_rank != five or len(cards_) - j < 5:
                break
            else:
                i = j

    # Four of a kind
    higher_suit = sorted(cards_, key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)
    i = 0
    for j in range(1, len(cards_)):
        if Card.ranks[higher_suit[i].rank][-1] == Card.ranks[higher_suit[j].rank][-1]:
            next_j = j + 1
            if next_j - i >= 4:
                hand_ = higher_suit[i:next_j]
                if j < 4:
                    hand_.append(higher_suit[next_j])
                else:
                    hand_.append(higher_suit[0])
                return 'Four of a kind', hand_
        elif len(cards_) - j < 5 - 1:
            break
        else:
            i = j

    # Full house
    a_high = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][-1], reverse=True)
    length_cards = len(cards_)
    hand_ = [a_high[0]]
    breakpoint_ = length_cards - 5
    pair_later = False
    for i in range(1, length_cards):
        length_hand = len(hand_)
        if i - length_hand > breakpoint_:
            break
        card = a_high[i]
        if Card.ranks[card.rank][-1] == Card.ranks[hand_[-1].rank][-1]:
            hand_.append(card)
            length_hand = len(hand_)
            if length_hand >= 5:
                if pair_later:
                    return 'Full house', hand_
                return 'Full house', hand_[2:] + hand_[:2]
            if length_hand == 3:
                pair_later = True
        elif length_hand > 3:
            if pair_later:
                hand_[3] = card
            else:
                hand_[2] = card
                hand_.pop()
        elif length_hand == 3:
            if pair_later:
                hand_.append(card)
            else:
                hand_[2] = card
        elif length_hand >= 2:
            hand_.append(card)
        else:
            hand_ = [card]

    # Flush
    suit_a_high = sorted(cards_, key=lambda card_: (card_.suit, Card.ranks[card_.rank][-1]), reverse=True)
    hand_ = [suit_a_high[0]]
    for i in range(1, length_cards):
        if i - len(hand_) > breakpoint_:
            break
        card = suit_a_high[i]
        if card.suit == hand_[-1].suit:
            hand_.append(card)
            if len(hand_) == 5:
                return 'Flush', hand_
        else:
            hand_ = [card]

    # High Straight
    hand_ = [a_high[0]]
    rank_five = Card.ranks['5'][-1]
    for i in range(1, length_cards):
        if Card.ranks[hand_[0].rank][-1] <= rank_five or i - len(hand_) > breakpoint_:
            break
        card = a_high[i]
        rank_card = Card.ranks[card.rank][-1]
        rank_last = Card.ranks[hand_[-1].rank][-1]
        if rank_card == rank_last - 1:
            hand_.append(card)
            if len(hand_) == 5:
                return 'Straight', hand_
        elif rank_card < rank_last:
            hand_ = [card]

    # Lowest Straight
    a_low = sorted(cards_, key=lambda card_: Card.ranks[card_.rank][0], reverse=True)
    hand_ = [a_low[0]]
    for i in range(1, length_cards):
        if Card.ranks[hand_[0].rank][0] != rank_five or i - len(hand_) > breakpoint_:
            break
        card = a_low[i]
        rank_card = Card.ranks[card.rank][0]
        rank_last = Card.ranks[hand_[-1].rank][0]
        if rank_card == rank_last - 1:
            hand_.append(card)
            if len(hand_) == 5:
                return 'Straight', hand_
        elif rank_card < rank_last:
            hand_ = [card]

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
for _ in range(30000):
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
    print(f'{name}: {count / total * 100}%')
