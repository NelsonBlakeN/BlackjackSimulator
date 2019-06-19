import strategy

from .hand import Hand

class Player(object):
    def __init__(self):
        self.hands = []
        self.results = []

        self.hands.append(Hand())

    def split(self, hand, shoe):
        new_hand = Hand()
        new_hand.deal(hand.pop())
        self.hands.append(new_hand)
        for hand in self.hands:
            if len(hand) is 2:
                shoe.deal(self.hands)

    def play(self, shoe, show_card):
        move = ''

        # Keep playing until stand
        for hand in self.hands:
            while move is not 'stand':
                if hand.total > 21:
                    break

                # Pair
                if len(hand) is 2 and hand[0] == hand[1]:
                    pair_card = hand[0]
                    move = strategy.pairs[pair_card][show_card]

                # Soft total
                elif len(hand) is 2 and any(card is 11 for card in hand):
                    if hand.total >= 19:
                        move = 'stand'
                    else:
                        non_ace = hand[0] if hand[0] is not 11 else hand[1]
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
                    self.split(hand, shoe)
                elif move is 'double':
                    shoe.deal(hand)
                    move = 'stand'