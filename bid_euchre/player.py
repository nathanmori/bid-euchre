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
    def bid(self, bids):
        pass

    @abstractmethod
    def play_trick(self, played_cards):
        pass


class CPUPlayer(Player):

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

    def play_trick(self, played_cards):
        if played_cards:
            led_card = played_cards[0]
        for card_i, card in enumerate(self.cards):
            if card.suit == led_card.suit:
                return self.cards.pop(card_i)
        else:
            return self.cards.pop()


class UserPlayer(Player):

    def bid(self, bids):
        print(bids)

        tricks = input('tricks >')
        call = input('call >')
        bid = Bid(tricks, call)

        last_bid_tricks = get_last_bid_tricks(bids)
        if bid.tricks > last_bid_tricks:
            return bid
        else:
            return None
        pass

    def play_trick(self, played_cards):
        pass
