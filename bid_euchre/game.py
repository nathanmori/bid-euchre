"""Game."""

import random

from bid_euchre.deck import RANKS, Deck
from bid_euchre.player import CPUPlayer, UserPlayer


N_TRICKS = 6
N_PLAYERS = 4
WIN_SCORE = 32


rank_i = {rank: i for i, rank in enumerate(RANKS)}


def beats(rank, other_rank, low):
    """Determine if rank beats other_rank.

    Args:
        rank (int/str)
        other_rank (int/str)
        low (bool): Indicates if low rank takes.
    """
    i = rank_i[rank]
    other_i = rank_i[other_rank]
    if low:
        return i < other_i
    else:
        return i > other_i


def get_taking_i(cards, trump, low):
    """Get index of taking card in cards.

    Args:
        cards (list of Card): Cards played.
        trump (str/None): Trump suit.
        high (bool): Indicates if low rank takes.
    """
    if trump is not None or any(card.suit == trump for card in cards):
        winning_suit = trump
    else:
        winning_suit = cards[0].suit

    taking_rank = cards[0].rank
    taking_i = 0
    for i, card in enumerate(cards):
        if card.suit == winning_suit and beats(card.rank, taking_rank):
            taking_rank = card.rank
            taking_i = i
    return taking_i


class Game:

    def __init__(self):
        self.players = [
            UserPlayer(self, 0),
            CPUPlayer(self, 1),
            CPUPlayer(self, 0),
            CPUPlayer(self, 1),
        ]
        self.team_scores = [0, 0]

    def play_hand(self, players):
        # deal
        deck = Deck(min_rank=7)
        for _ in range(N_TRICKS):
            for player in players:
                card = deck.draw()
                player.deal(card)

        # bid
        bids = []
        for player in players:
            bid = player.bid(bids)
            bids.append(bid)
        for player, bid in list(zip(players, bids))[::-1]:
            if bid is not None:
                if bid.call == 'high':
                    trump = None
                    low = False
                elif bid.call == 'low':
                    trump = None
                    low = True
                else:
                    trump = bid.call
                    low = False
                calling_team = player.team
                noncalling_team = (calling_team + 1) % 2
                break
        else:
            raise ValueError('no bid')

        # play tricks
        team_tricks = [0, 0]
        for _ in range(N_TRICKS):
            trick_cards = []
            for player in players:
                trick_cards.append(player.play_trick(trick_cards))

            taking_i = get_taking_i(trick_cards, trump, low)
            taking_player = players[taking_i]
            taking_team = taking_player.team
            team_tricks[taking_team] += 1

            players = players[taking_i:] + players[:taking_i]

        # update score
        if team_tricks[calling_team] >= bid.tricks:
            self.team_scores[calling_team] += team_tricks[calling_team]
        else:
            self.team_scores[calling_team] -= bid.tricks
        self.team_scores[noncalling_team] += team_tricks[noncalling_team]

    def play(self):
        first = random.choice(range(N_PLAYERS))
        while max(self.team_scores) < WIN_SCORE:
            players = self.players[first:] + self.players[:first]
            self.play_hand(players)
            first += 1
            first %= N_PLAYERS


if __name__ == '__main__':
    Game().play()
