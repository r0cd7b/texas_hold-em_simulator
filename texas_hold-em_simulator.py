import random


class Card:
    """
    ranks = {
        '2': (1,),
        '3': (2,),
        '4': (3,),
        '5': (4,),
        '6': (5,),
        '7': (6,),
        '8': (7,),
        '9': (8,),
        '10': (9,),
        'J': (10,),
        'Q': (11,),
        'K': (12,),
        'A': (0, 13)
    }
    """
    ranks = {
        'Q': (11,),
        'K': (12,),
        'A': (0, 13)
    }
    suits = {'♠': 0, '♣': 1, '♥': 2, '♦': 3}

    def __init__(self):
        self.rank, self.suit = rank, suit

    def __repr__(self):
        return self.rank + self.suit


def seek_best(seven_cards_):
    # Straight flush 찾기
    seven_cards_.sort(key=lambda card_: (card_.suit, Card.ranks[card_.rank][-1]), reverse=True)
    starting, stopping = 0, len(seven_cards_) - 5
    for i_ in range(1, len(seven_cards_)):
        previous_i = i_ - 1
        if Card.ranks[seven_cards_[previous_i].rank][-1] - 1 == Card.ranks[seven_cards_[i_].rank][-1] and \
                seven_cards_[previous_i].suit == seven_cards_[i_].suit:
            next_i = i_ + 1
            if next_i - starting == 5:
                return seven_cards_[starting:next_i], 'Straight flush'
        elif i_ > stopping:
            break
        else:
            starting = i_

    # Lowest straight flush 찾기
    seven_cards_.sort(key=lambda card_: (card_.suit, Card.ranks[card_.rank][0]), reverse=True)
    five = -1
    for i_, card in enumerate(seven_cards_):
        if card.rank == '5':
            if i_ > stopping:
                break
            five = i_
        elif five > -1:
            previous_i = i_ - 1
            if Card.ranks[seven_cards_[previous_i].rank][0] - 1 == Card.ranks[seven_cards_[i_].rank][0] and \
                    seven_cards_[previous_i].suit == seven_cards_[i_].suit:
                next_i = i_ + 1
                if next_i - five == 5:
                    return seven_cards_[five:next_i], 'Straight flush'
            elif i_ > stopping:
                break
            else:
                five = -1

    # Four of a kind 찾기
    seven_cards_.sort(key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)
    starting, stopping = 0, len(seven_cards_) - 4
    for i_ in range(1, len(seven_cards_)):
        previous_i = i_ - 1
        if seven_cards_[previous_i].rank == seven_cards_[i_].rank:
            next_i = i_ + 1
            if next_i - starting == 4:
                if starting == 0:
                    return seven_cards_[starting:starting + 5], 'Four of a kind'
                else:
                    best_five_ = seven_cards_[starting:starting + 4]
                    best_five_.append(seven_cards_[0])
                    return best_five_, 'Four of a kind'
        elif i_ > stopping:
            break
        else:
            starting = i_

    return [], ''


players = 2

cards = []
for rank in Card.ranks:
    for suit in Card.suits:
        cards.append(Card())
random.shuffle(cards)

hole = tuple([] for _ in range(players))
for _ in range(2):
    for i in range(players):
        hole[i].append(cards.pop())

community = []
cards.pop()
for _ in range(3):
    community.append(cards.pop())
for _ in range(2):
    cards.pop()
    community.append(cards.pop())

hands = {
    'High card': 0,
    'Pair': 1,
    'Two pairs': 2,
    'Three of a kind': 3,
    'Straight': 4,
    'Flush': 5,
    'Full house': 6,
    'Four of a kind': 7,
    'Straight flush': 8
}
for i in range(players):
    seven_cards = hole[i] + community
    best_five, hand = seek_best(seven_cards)
    print(seven_cards)
    print(best_five, hand)
    print()
