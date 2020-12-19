from JJMumbleBot.plugins.extensions.blackjack.utility import settings
from JJMumbleBot.plugins.extensions.blackjack.utility.card import Deck
from JJMumbleBot.plugins.extensions.blackjack.utility.player import Player
from JJMumbleBot.lib.utils.runtime_utils import get_bot_name
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.utils.runtime_utils import get_command_token
from JJMumbleBot.lib.resources.strings import C_PGUI_SETTINGS, P_TXT_IND_COL, P_TXT_SUBHEAD_COL
from time import sleep


def prepare_new_game():
    settings.game_users = {}
    settings.dealer = None
    settings.deck = None
    settings.game_host = None
    settings.current_player = None
    settings.game_user_cycle = None
    settings.player_counter = 0


def stop_game():
    settings.dealer = None
    settings.deck = None
    settings.game_host = None
    settings.game_started = False
    settings.game_waiting = False
    settings.lobby_users = {}
    settings.game_users = {}
    settings.current_player = None
    settings.game_user_cycle = None
    settings.player_counter = 0


def next_player():
    if settings.game_started and len(settings.game_users) > 0:
        settings.player_counter += 1
        if settings.player_counter > len(settings.game_users) - 1:
            settings.player_counter = 0
        settings.current_player = settings.game_users[list(settings.game_users)[settings.player_counter]]

        total_passes = 0
        while (settings.current_player.is_bust or
               settings.current_player.is_blackjack or
               settings.current_player.is_stay) and (total_passes < len(list(settings.game_users))):
            total_passes += 1
            settings.player_counter += 1
            if settings.player_counter > len(settings.game_users) - 1:
                settings.player_counter = 0

        if total_passes >= len(list(settings.game_users)):
            dealer_turn()
            return
        settings.current_player = settings.game_users[list(settings.game_users)[settings.player_counter]]
        gs.gui_service.quick_gui(f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>{settings.current_player.player}'s</font> turn:",
                                 text_type='header', box_align='left', text_align='left')


def dealer_turn():
    # Dealer hits or stays:
    player_avg_ratio = sum(
        [settings.game_users[player].hand_total() if not settings.game_users[player].is_bust else 0 for player in
         settings.game_users]) / len(
        list(settings.game_users))

    if player_avg_ratio > 21:
        settings.dealer.stay()
        gs.gui_service.quick_gui(f"The <font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Dealer</font> "
                                 f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>STAYS</font>"
                                 f"<br><br>{get_blackjack_table(hide_dealer=False)}",
                                 text_type='header', box_align='left', text_align='left')
        sleep(2)

    while not settings.dealer.is_bust and not settings.dealer.is_stay and not settings.dealer.is_blackjack:
        while settings.dealer.hand_total() < 15 or (
                settings.dealer.hand_total() < player_avg_ratio and settings.dealer.hand_total() < 21):
            settings.dealer.hand.add_card(settings.deck.DrawCard())
            gs.gui_service.quick_gui(f"The <font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Dealer</font> "
                                     f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>HITS</font>"
                                     f"<br><br>{get_blackjack_table(hide_dealer=False)}",
                                     text_type='header', box_align='left', text_align='left')
            sleep(2)

        if settings.dealer.hand_total() > 21:
            settings.dealer.bust()
        elif settings.dealer.hand_total() == 21:
            settings.dealer.blackjack()
        else:
            settings.dealer.stay()
    game_over()


def hit(double_down=False):
    settings.current_player.hand.add_card(settings.deck.DrawCard())
    if settings.current_player.hand_total() > 21:
        settings.current_player.bust()
        gs.gui_service.quick_gui(
            f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>{settings.current_player.player}<font> "
            f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>BUSTED!</font><br><br>{get_blackjack_table()}",
            text_type='header', box_align='left', text_align='left')
        if double_down:
            stay()
        else:
            next_player()
    elif settings.current_player.hand_total() == 21:
        settings.current_player.blackjack()
        gs.gui_service.quick_gui(
            f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>{settings.current_player.player}</font> has "
            f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>BLACKJACK!</font><br><br>{get_blackjack_table()}",
            text_type='header', box_align='left', text_align='left')
        if double_down:
            stay()
        else:
            next_player()
    else:
        if double_down:
            gs.gui_service.quick_gui(
                f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>{settings.current_player.player}</font> has "
                f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>DOUBLED DOWN!</font><br><br>{get_blackjack_table()}",
                text_type='header', box_align='left', text_align='left')
            stay()
        else:
            gs.gui_service.quick_gui(
                f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>{settings.current_player.player}</font> has "
                f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>HIT!</font><br><br>{get_blackjack_table()}",
                text_type='header', box_align='left', text_align='left')


def stay():
    settings.current_player.stay()
    next_player()


def double():
    settings.current_player.bet *= 2
    hit(double_down=True)


def game_over():
    out_str = f""
    if settings.dealer.is_bust:
        out_str += f"The <font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Dealer</font> has " \
                   f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>BUST!</font><br><br>"
    elif settings.dealer.is_blackjack:
        out_str += f"The <font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Dealer</font> has " \
                   f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>BLACKJACK!</font><br><br>"
    out_str += f"{get_blackjack_table(hide_dealer=False)}<br><br>"
    out_str += f"<br><font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Hand total for dealer:</font> " \
               f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>[{settings.dealer.hand_total()}]</font> -> Bet: ${settings.dealer.bet:.2f}"
    for i, player in enumerate(settings.game_users):

        # Calculate winnings/losses:

        return_amount = 0
        # Dealer busts and player does not bust:
        if settings.dealer.is_bust and not settings.game_users[player].is_bust:
            return_amount = settings.game_users[player].bet * (3 / 2)
        # Dealer blackjacks and player does not:
        elif settings.dealer.is_blackjack and not settings.game_users[player].is_blackjack:
            return_amount = 0
        # Player has blackjack and dealer does not:
        elif settings.game_users[player].is_blackjack and not settings.dealer.is_blackjack:
            return_amount = settings.game_users[player].bet * (3 / 2)
        # Dealer blackjacks and player does as well: (push)
        elif settings.dealer.is_blackjack and settings.game_users[player].is_blackjack:
            return_amount = settings.game_users[player].bet
        # Player busts:
        elif settings.game_users[player].is_bust:
            return_amount = 0
        elif settings.game_users[player].hand_total() > settings.dealer.hand_total():
            return_amount = settings.game_users[player].bet * (3 / 2)
        elif settings.dealer.hand_total() > settings.game_users[player].hand_total():
            return_amount = 0
        else:
            return_amount = -1

        out_str += f"<br><font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Hand total for {player}:</font> <font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>[{settings.game_users[player].hand_total()}]</font> -> Bet: ${settings.game_users[player].bet:.2f} - Return: ${return_amount:.2f}"
    gs.gui_service.quick_gui(
        [out_str, f"<br>Play again? Create a lobby: {get_command_token()}startblackjack"],
        text_type='header', box_align='left', text_align='left')
    stop_game()


def get_blackjack_table(hide_dealer=True):
    if settings.game_started:
        table_str = "Blackjack Table:<br><br>"
        if hide_dealer:
            table_str += f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Dealer:</font> " \
                         f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>{str(settings.dealer.hand.cards[0].value)}, #</font>"
        else:
            table_str += f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Dealer:</font> " \
                         f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>{', '.join(str(card.value) for card in settings.dealer.hand.cards)}</font>"
        for i, player in enumerate(settings.game_users):
            table_str += f"<br><font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>{player}[{settings.game_users[player].hand_total()}]:</font> " \
                         f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>{', '.join(str(card.value) for card in settings.game_users[player].hand.cards)}</font>"
        return table_str
    return None


def create_new_game():
    # Create a main deck of 7 decks of cards.
    settings.deck = Deck()
    for i in range(7):
        settings.deck.cards.extend(Deck().cards)
    settings.deck.ShuffleDeck()
    # Create all players.
    settings.game_users = {}
    for i, player in enumerate(settings.lobby_users):
        settings.game_users[player] = Player(player, settings.lobby_users[player])

    # Draw 2 cards for each player and the dealer.
    for i, player in enumerate(settings.game_users):
        settings.game_users[player].hand.add_card(settings.deck.DrawCard())
        settings.game_users[player].hand.add_card(settings.deck.DrawCard())

    # Create the bot dealer
    from random import seed, randint
    from os import urandom
    seed(int.from_bytes(urandom(8), byteorder="big"))

    settings.dealer = Player(get_bot_name(), randint(settings.min_bet, settings.max_bet))
    settings.dealer.hand.add_card(settings.deck.DrawCard())
    settings.dealer.hand.add_card(settings.deck.DrawCard())

    # Set the current player's turn.
    settings.current_player = settings.game_users[list(settings.game_users)[0]]
