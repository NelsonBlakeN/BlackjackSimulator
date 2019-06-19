import strategy

from .hand import Hand

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