"""Card deck."""

RANKS = [*range(2, 11), *'JQKA']
SUITS = 'scdh'
SYMBOLS = '♠♣♦♥'
suit_symbols = dict(zip(SUITS, SYMBOLS))


class Card:
    """Card.

    Args:
        rank (int/str)
        suit (str)
    """

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


class Deck:
    """Deck of cards.

    Args:
        min_rank (int/str): Defaults to 2.
        max_rank (int/str): Defaults to 'A'.
    """


    def __init__(self, min_rank=2, max_rank='A'):
        min_rank_ix = RANKS.index(min_rank)
        max_rank_ix = RANKS.index(max_rank)
        if max_rank_ix <= min_rank_ix:
            raise ValueError('max_rank_ix must be > min_rank_ix')
        self.ranks = RANKS[min_rank_ix:max_rank_ix]

        self.cards = [Card(rank, suit)
                      for rank in self.ranks for suit in SUITS]
        self.shuffle

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
