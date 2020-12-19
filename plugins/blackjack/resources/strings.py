from JJMumbleBot.lib.utils.runtime_utils import get_command_token
from JJMumbleBot.plugins.extensions.blackjack.utility.settings import min_bet, max_bet

###########################################################################
# BLACKJACK PLUGIN CONFIG PARAMETER STRINGS

# COMMAND ERROR STRINGS
CMD_INVALID_JOIN = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}bet 'bet_amount' (${min_bet} to ${max_bet})"
]
CMD_INVALID_BET = f"ERROR: Invalid Bet! All bets must be between ${min_bet} and ${max_bet}."
# GAME ERROR STRINGS
GAME_ALREADY_STARTED = "A Blackjack game is already in progress, so a new one cannot be started."
GAME_STARTED_JOIN = "A Blackjack game is already in progress!"
GAME_LOBBY_OPEN = f"A Blackjack game lobby is open. Use [{get_command_token()}bet 'bet_amount'] to join!"
GAME_LOBBY_FULL = "The Blackjack game lobby is full!"
GAME_STOPPED_MANUAL = f"The Blackjack game has been manually stopped by the session leader or administrator."
GAME_LOBBY_CLOSED_MANUAL = f"The Blackjack game lobby has been closed by the session leader or administrator."
GAME_START_ERROR = "Only the game lobby session leader can start the Blackjack game."
