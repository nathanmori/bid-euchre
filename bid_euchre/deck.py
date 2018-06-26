"""Card deck."""

class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


class Deck:

    ranks = [*range(2, 11), *'JQKA']
    suits = 'scdh'
    symbols = '♠♣♦♥'
    suit_symbols = dict(zip(suits, symbols))

    def __init__(self, min_rank=2, max_rank='A'):
        min_rank_ix = self.ranks.index(min_rank)
        max_rank_ix = self.ranks.index(max_rank)
        if max_rank_ix <= min_rank_ix:
            raise ValueError('max_rank_ix must be > min_rank_ix')
        self.ranks = self.ranks[min_rank_ix, max_rank_ix]

        self.cards = [
            Card(rank, suit) for rank in self.ranks for suit in self.suits
        ]
        self.shuffle

    def shuffle(self):
        random.shuffle(self.cards)
