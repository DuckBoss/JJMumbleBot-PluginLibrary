from typing import Union
from random import shuffle, seed
from os import urandom


class Card:
    def __init__(self, card_value: Union[str, int], card_suit: str):
        if card_value in ["K", "J", "Q", "A"]:
            self.value = card_value
        elif card_value in range(2, 11):
            self.value = str(card_value)
        else:
            self.value = None

        if card_suit in ["Spades", "Hearts", "Diamonds", "Clubs"]:
            self.suit = card_suit
        else:
            self.suit = None

    def __str__(self):
        return f"[{self.suit}-{self.value}]"


class Deck:
    def __init__(self):
        self.cards = []
        self._createDeck()

    def _createDeck(self):
        for i in ["Spades", "Hearts", "Diamonds", "Clubs"]:
            self.cards.append(Card("K", i))
            self.cards.append(Card("J", i))
            self.cards.append(Card("Q", i))
            self.cards.append(Card("A", i))
            for j in range(2, 11):
                self.cards.append(Card(j, i))
        self.ShuffleDeck()

    def ShuffleDeck(self):
        for i in range(5):
            seed(int.from_bytes(urandom(8), byteorder="big"))
            shuffle(self.cards)

    def DrawCard(self) -> Card:
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            self.cards.extend(self._createDeck())
            self.ShuffleDeck()

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)
