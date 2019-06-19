import random
from itertools import repeat

class Shoe:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        decks = self._generate_decks(num_decks)
        self._shuffle(decks)

    def _generate_decks(self, num_decks):
        # Create single deck
        vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
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