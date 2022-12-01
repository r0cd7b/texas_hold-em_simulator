import random
import timeit


class Card:
    # '♠': 0, '♣': 1, '♥': 2, '♦': 3
    ranks = {'A': (0, 13), '2': (1,), '3': (2,), '4': (3,), '5': (4,), '6': (5,), '7': (6,), '8': (7,), '9': (8,),
             '10': (9,), 'J': (10,), 'Q': (11,), 'K': (12,)}
    suits = {'♠': 0, '♣': 1, '♥': 2, '♦': 3}

    def __init__(self):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return self.rank + self.suit


def seek_best(seven_cards_):
    # Straight flush 찾기
    seven_cards_.sort(key=lambda card_: (card_.suit, Card.ranks[card_.rank][-1]), reverse=True)
    best_ = [seven_cards_[0]]
    for i_ in range(1, len(seven_cards_)):
        if seven_cards_[i_].suit == best_[-1].suit and Card.ranks[seven_cards_[i_].rank][-1] == \
                Card.ranks[best_[-1].rank][-1] - 1:
            best_.append(seven_cards_[i_])
            if len(best_) == 5:
                return best_, 'Straight flush'
        elif i_ <= len(seven_cards_) - 5:
            best_ = [seven_cards_[i_]]
        else:
            break

    # Lowest straight flush 찾기
    suit_a_0 = sorted(seven_cards_, key=lambda card_: (card_.suit, Card.ranks[card_.rank][0]), reverse=True)
    best_ = []
    for i_, card in enumerate(suit_a_0):
        if card.rank == '5':
            if i_ <= len(seven_cards_) - 5:
                best_ = [card]
            else:
                break
        elif best_ and card.suit == best_[-1].suit and Card.ranks[card.rank][0] == \
                Card.ranks[best_[-1].rank][0] - 1:
            best_.append(card)
            if len(best_) == 5:
                return best_, 'Straight flush'

    # Four of a kind 찾기
    # starting = 0
    # a_high_suit = sorted(seven_cards_, key=lambda card_: (Card.ranks[card_.rank][-1], card_.suit), reverse=True)
    # best_.clear()
    # while starting < 4:
    #     for i in range(starting, 7):

    return seven_cards_[:5], 'High card'


players = 2

cards = []
for rank in Card.ranks:
    for suit in Card.suits:
        cards.append(Card())

random.shuffle(cards)

hands = tuple([cards.pop(), cards.pop()] for _ in range(players))
cards.pop()
community = [cards.pop(), cards.pop(), cards.pop()]
cards.pop()
community.append(cards.pop())
cards.pop()
community.append(cards.pop())

for i in range(players):
    hands[i].extend(community)
    print(hands[i])
    best, hand = seek_best(hands[i])
    print(best, hand)
    print()
