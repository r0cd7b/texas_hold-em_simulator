import random
import time
from collections import deque


class Card:
    """
    ranks = {'A': (0, 13), '2': (1,), '3': (2,), '4': (3,), '5': (4,), '6': (5,), '7': (6,), '8': (7,), '9': (8,),
             '10': (9,), 'J': (10,), 'Q': (11,), 'K': (12,)}
    suits = {'♠': 0, '♣': 1, '♥': 2, '♦': 3}
    """
    ranks = {'A': (0, 13), '2': (1,), '3': (2,), '4': (3,), '5': (4,), '6': (5,), '7': (6,), '8': (7,), '9': (8,),
             '10': (9,), 'J': (10,), 'Q': (11,), 'K': (12,)}
    suits = {'♠': 0, '♣': 1, '♥': 2, '♦': 3}

    def __init__(self, rank_, suit_):
        self.rank = rank_
        self.suit = suit_

    def __repr__(self):
        return self.rank + self.suit


def seek_hand(cards_):
    # Straight flush 검사
    a_highest = sorted(cards_, key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)
    cards_deque = deque(a_highest)
    while Card.ranks[cards_deque[0].rank][-1] > Card.ranks['5'][-1] and len(cards_deque) >= 5:
        hand_ = [cards_deque.popleft()]
        for _ in range(len(cards_deque)):
            card = cards_deque.popleft()
            if Card.ranks[card.rank][-1] == Card.ranks[hand_[-1].rank][-1] - 1 and card.suit == hand_[-1].suit:
                hand_.append(card)
                if len(hand_) == 5:
                    return hand_, 'Straight flush'
            else:
                cards_deque.append(card)

    # Lowest straight flush 검사
    a_lowest = sorted(a_highest, key=lambda card_: (Card.ranks[card_.rank][0], card_.suit), reverse=True)
    cards_deque = deque(a_lowest)
    while cards_deque[0].rank == '5' and len(cards_deque) >= 5:
        hand_ = [cards_deque.popleft()]
        for _ in range(len(cards_deque)):
            card = cards_deque.popleft()
            if Card.ranks[card.rank][0] == Card.ranks[hand_[-1].rank][0] - 1 and card.suit == hand_[-1].suit:
                hand_.append(card)
                if len(hand_) == 5:
                    return hand_, 'Straight flush'
            else:
                cards_deque.append(card)

    # Four of a kind 검사
    cards_deque = deque(a_highest)
    while len(cards_deque) >= 5:
        hand_ = [cards_deque.popleft()]
        for _ in range(len(cards_deque)):
            card = cards_deque.popleft()
            if Card.ranks[card.rank][0] == Card.ranks[hand_[-1].rank][0]:
                hand_.append(card)
            else:
                cards_deque.append(card)
        if len(hand_) == 4:
            hand_.append(cards_deque.popleft())
            return hand_, 'Four of a kind'

    # Full house 검사
    cards_deque = deque(a_highest)
    while len(cards_deque) >= 5:
        hand_ = [cards_deque.popleft()]
        for _ in range(len(cards_deque)):
            card = cards_deque.popleft()
            if Card.ranks[card.rank][0] == Card.ranks[hand_[-1].rank][0]:
                hand_.append(card)
            else:
                cards_deque.append(card)
        if len(hand_) == 4:
            hand_.append(cards_deque.popleft())
            return hand_, 'Full house'

    # Flush 검사
    # 정렬 상태 2개만 쓰기 ((A가 높을 때, 문양), (A가 낮을 때, 문양))
    # deque와 pop, append 방식으로 검사

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
        if name == 'Full house':
            print(time.perf_counter_ns() - t)
            print(cards, hand, name)
            break
    else:
        continue
    break
