from .player import Player

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

