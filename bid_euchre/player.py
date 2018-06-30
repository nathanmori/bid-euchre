"""Players."""

from abc import abstractmethod, ABC

from .bid import Bid
from .deck import SUITS


def get_last_bid_tricks(bids):
    try:
        last_bid_tricks = next(
            bid.tricks for bid in bids[::-1] if bid is not None)
    except StopIteration:
        last_bid_tricks = 0
    return last_bid_tricks


class Player(ABC):

    def __init__(self, game, team):
        self.game = game
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

        high_winners = sum(1 for card in self.cards if card.rank == 'A')
        low_winners = sum(1 for card in self.cards if card.rank == 7)
        suits_winners = [
            sum(1 for card in self.cards
                if card.rank == 'J' and card.suit == suit)
            for suit in SUITS
        ]

        max_winners = max(high_winners, low_winners, *suits_winners)

        if max_winners == high_winners:
            bid = Bid(high_winners, 'high')
        elif max_winners == low_winners:
            bid = Bid(low_winners, 'low')
        else:
            for suit, suit_winners in zip(SUITS, suits_winners):
                if max_winners == suit_winners:
                    break
            bid = Bid(suit_winners, suit)

        last_bid_tricks = get_last_bid_tricks(bids)
        if bid.tricks > last_bid_tricks:
            return bid
        else:
            return None


class UserPlayer(Player):

    def play_trick(self, played_cards):
        pass

    def bid(self, bids):
        pass
