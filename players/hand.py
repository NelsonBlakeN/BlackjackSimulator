class Hand(list):
    def __init__(self):
        super().__init__()

    @property
    def total(self):
        if not any(card == 11 for card in self):
            return sum(self)
        else:
            not_aces = []
            aces = 0
            for card in self:
                if card is not 11:
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
        return any(card == 11 for card in self)