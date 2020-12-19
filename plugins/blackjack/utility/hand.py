from JJMumbleBot.plugins.extensions.blackjack.utility.card import Card


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card: Card) -> bool:
        self.cards.append(card)

    def hand_total(self) -> int:
        total = 0
        num_of_ace = 0
        for card in self.cards:
            if card.value in ["K", "Q", "J"]:
                total += 10
            elif card.value in ["A"]:
                num_of_ace += 1
            else:
                total += int(card.value)

        ace_counter = num_of_ace
        for i in range(num_of_ace):
            if (total + (ace_counter * 11)) > 21 or (total + ace_counter) < 10:
                total += 1
                ace_counter -= 1
            else:
                total += 11

        return total

    def clear_hand(self):
        self.cards = []

