"""Players."""

from abc import abstractmethod

class Player:

    def __init__(self, team):
        self.team = team
        self.cards = []

    def deal(self, card):
        self.cards.append(card)

    @abstractmethod
    def play_trick(self, played_cards):
        pass

    @abstractmethod
    def bid(self, bids):
        pass


class CPUPlayer(Player):

    def play_trick(self, played_cards):
        pass

    def bid(self, bids):
        pass


class UserPlayer(Player):

    def play_trick(self, played_cards):
        pass

    def bid(self, bids):
        pass
