import random
import time


class Card:
    """
    ranks = {'A': (0, 13), '2': (1,), '3': (2,), '4': (3,), '5': (4,), '6': (5,), '7': (6,), '8': (7,), '9': (8,),
             '10': (9,), 'J': (10,), 'Q': (11,), 'K': (12,)}
    suits = {'♠': 0, '♣': 1, '♥': 2, '♦': 3}
    """
    ranks = {'A': (0, 13), '2': (1,), '3': (2,), '4': (3,), '5': (4,), '6': (5,), '7': (6,), '8': (7,), '9': (8,),
             '10': (9,), 'J': (10,), 'Q': (11,), 'K': (12,)}
    suits = {'♠': 0, '♣': 1, '♥': 2, '♦': 3}

    def __init__(self):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return self.rank + self.suit


def seek_hand(cards_):
    # Straight flush 검사
    cards_.sort(key=lambda card_: (card_.suit, Card.ranks[card_.rank][-1]), reverse=True)
    for i_ in range(len(cards_) - 4):
        for j in range(i_, i_ + 4):
            if Card.ranks[cards_[j].rank][-1] != Card.ranks[cards_[j + 1].rank][-1] + 1 or cards_[j].suit != \
                    cards_[j + 1].suit:
                break
        else:
            return cards_[i_:i_ + 5], 'Straight flush'

    # Lowest straight flush 검사
    cards_.sort(key=lambda card_: (card_.suit, Card.ranks[card_.rank][0]), reverse=True)
    for i_ in range(len(cards_) - 4):
        if cards_[i_].rank == '5':
            for j in range(i_, i_ + 4):
                if Card.ranks[cards_[j].rank][0] != Card.ranks[cards_[j + 1].rank][0] + 1 or cards_[j].suit != \
                        cards_[j + 1].suit:
                    break
            else:
                return cards_[i_:i_ + 5], 'Four of a kind'

    # Four of a kind 검사
    cards_.sort(key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)
    for i_ in range(len(cards_) - 3):
        for j in range(i_, i_ + 3):
            if Card.ranks[cards_[j].rank][-1] != Card.ranks[cards_[j + 1].rank][-1]:
                break
        else:
            hand_ = cards_[i_:i_ + 4]
            if i_ <= 0:
                hand_.append(cards_[i_ + 4])
            else:
                hand_.append(cards_[0])
            return hand_, 'Four of a kind'

    # Full house 검사
    hand_ = []
    for length in (3, 2):
        for i_ in range(len(cards_) - length + 1):
            for j in range(i_, i_ + length - 1):
                if Card.ranks[cards_[j].rank][-1] != Card.ranks[cards_[j + 1].rank][-1]:
                    break
            else:
                end = i_ + length
                hand_.extend(cards_[i_:end])
                cards_ = cards_[:i_ + 1] + cards_[end:]
                break
        else:
            break
    else:
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
            deck.append(Card())

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
