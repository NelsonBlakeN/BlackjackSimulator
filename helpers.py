import strategy

class Player(object):
    def __init__(self):
        self.hands = []
        self.results = []

        self.hands.append(Hand())

    def play(self, shoe, show_card):
        move = ''

        # Keep playing until stand
        for hand in self.hands:
            while move is not 'stand':
                if hand.total > 21:
                    break

                # Pair
                if len(hand) is 2 and hand[0] is hand[1]:
                    pair_card = hand[0]
                    move = strategy.pairs[pair_card][show_card]

                # Soft total
                elif len(hand) is 2 and any(isinstance(card, tuple) for card in hand):
                    if hand.total >= 19:
                        move = 'stand'
                    else:
                        non_ace = hand[0] if type(hand[0]) is not tuple else hand[1]
                        move = strategy.soft_totals[non_ace][show_card]

                # Hard total
                else:
                    if hand.total >= 17:
                        move = 'stand'
                    else:
                        move = strategy.hard_totals[hand.total][show_card] # pylint: disable=E1136

                if move is 'hit':
                    shoe.deal(hand)
                elif move is 'split':
                    hand = [[hand[0]], [hand[1]]]
                    shoe.deal(hand)
                    for _ in hand:
                        self.play(shoe, show_card)
                elif move is 'double':
                    shoe.deal(hand)
                    move = 'stand'

class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.show_card = None
        self.hand = self.hands[0]

    @property
    def show_card(self):
        if type(self.__show_card) is tuple:
            return 11
        else:
            return self.__show_card

    @show_card.setter
    def show_card(self, val):
        self.__show_card = val

    @property
    def total(self):
        return self.hand.total

    def play(self, shoe):
        while self.hand.total < 17:
            shoe.deal(self.hand)

import random
from itertools import repeat

class Shoe:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        decks = self._generate_decks(num_decks)
        self._shuffle(decks)

    def _generate_decks(self, num_decks):
        # Create single deck
        vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, (1, 11)]
        deck = [v for value in vals for v in repeat(value, 4)]

        # Duplicate deck in single list
        return [c for card in deck for c in repeat(card, num_decks)]

    def _shuffle(self, decks):
        '''Shuffle cards'''
        self.shoe = []
        for _ in range(len(decks)):
            c = random.randint(0, len(decks)-1)
            self.shoe.append(decks.pop(c))

    def deal(self, hand):
        if len(self.shoe) > 0:
            hand.deal(self.shoe.pop())
        else:
            # Recreate shoe, then deal
            decks = self._generate_decks(self.num_decks)
            self._shuffle(decks)

            hand.deal(self.shoe.pop())

class Hand(list):
    def __init__(self):
        super().__init__()

    @property
    def total(self):
        if not any(isinstance(card, tuple) for card in self):
            return sum(self)
        else:
            not_aces = []
            aces = 0
            for card in self:
                if type(card) is not tuple:
                    not_aces.append(card)
                else:
                    aces += 1
            hand_sum = sum(not_aces)
            if hand_sum > 10:
                hand_sum += aces
            else:
                hand_sum += 11 + (aces-1)
            return hand_sum

    def deal(self, card):
        self.append(card)

    def has_ace(self):
        return any(isinstance(card, tuple) for card in self)
