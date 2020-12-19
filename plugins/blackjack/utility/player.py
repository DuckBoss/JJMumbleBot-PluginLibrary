from JJMumbleBot.plugins.extensions.blackjack.utility.hand import Hand


class Player:
    def __init__(self, player_name: str, bet_amount: float):
        self.player = player_name
        self.bet = bet_amount
        self.hand = Hand()
        self.has_bet = True
        self.is_stay = False
        self.is_bust = False
        self.is_blackjack = False

    def stay(self):
        self.is_stay = True

    def bust(self):
        self.is_bust = True

    def blackjack(self):
        self.is_blackjack = True

    def hand_total(self) -> int:
        return self.hand.hand_total()
