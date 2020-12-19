from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.plugins.extensions.blackjack.resources.strings import *
from JJMumbleBot.plugins.extensions.blackjack.utility import settings
from JJMumbleBot.plugins.extensions.blackjack.utility import blackjack_utility
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.privileges import privileges_check, Privileges


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        settings.game_started = False
        settings.blackjack_metadata = self.metadata
        log(
            INFO,
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.",
            origin=L_STARTUP,
            print_mode=PrintMode.REG_PRINT.value
        )

    def quit(self):
        log(
            INFO,
            f"Exiting {self.plugin_name} plugin...",
            origin=L_SHUTDOWN,
            print_mode=PrintMode.REG_PRINT.value
        )

    def cmd_stopblackjack(self, data):
        if settings.game_started:
            if settings.game_host == gs.mumble_inst.users[data.actor]['name'] or privileges_check(gs.mumble_inst.users[data.actor]['name']) >= Privileges.ADMINISTRATOR.value:
                blackjack_utility.stop_game()
                gs.gui_service.quick_gui(GAME_STOPPED_MANUAL,
                                         text_type='header', box_align='left')
        elif settings.game_waiting:
            if settings.game_host == gs.mumble_inst.users[data.actor]['name'] or privileges_check(gs.mumble_inst.users[data.actor]['name']) >= Privileges.ADMINISTRATOR.value:
                blackjack_utility.stop_game()
                gs.gui_service.quick_gui(GAME_LOBBY_CLOSED_MANUAL,
                                         text_type='header', box_align='left')

    def cmd_startblackjack(self, data):
        if settings.game_started:
            log(INFO, GAME_ALREADY_STARTED,
                origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(GAME_ALREADY_STARTED,
                                     text_type='header', box_align='left')
            return
        elif not settings.game_waiting:
            # If the game hasn't started, open the lobby for users to join.
            settings.game_waiting = True
            blackjack_utility.prepare_new_game()
            settings.game_host = gs.mumble_inst.users[data.actor]['name']
            gs.gui_service.quick_gui(GAME_LOBBY_OPEN,
                                     text_type='header', box_align='left')
        else:
            # If the game is ready to start, gather all the players in the lobby and start.
            if len(list(settings.lobby_users)) == 0:
                return
            settings.game_started = True
            settings.game_waiting = False
            if settings.game_host == gs.mumble_inst.users[data.actor]['name'] or privileges_check(gs.mumble_inst.users[data.actor]['name']) >= Privileges.ADMINISTRATOR.value:
                blackjack_utility.create_new_game()
                gs.gui_service.quick_gui(f"The Blackjack game has started with {len(list(settings.lobby_users))} users.",
                                         text_type='header', box_align='left')
                gs.gui_service.quick_gui(blackjack_utility.get_blackjack_table(),
                                         text_type='header', box_align='left')
                gs.gui_service.quick_gui(f"{settings.current_player.player}'s turn:",
                                         text_type='header', box_align='left')
            else:
                gs.gui_service.quick_gui(GAME_START_ERROR,
                                         text_type='header', box_align='left')

    def cmd_bet(self, data):
        split_data = data.message.strip().split(' ', 1)
        if len(split_data) != 2:
            log(ERROR, CMD_INVALID_JOIN,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(
                CMD_INVALID_JOIN,
                text_type='header',
                box_align='left', user=gs.mumble_inst.users[data.actor]['name'],
                ignore_whisper=True)
            return

        if settings.game_started:
            gs.gui_service.quick_gui(GAME_STARTED_JOIN,
                                     text_type='header', box_align='left', text_align='left',
                                     user=gs.mumble_inst.users[data.actor]['name'])
            return
        elif settings.game_waiting:
            if len(list(settings.lobby_users)) < settings.max_players:
                if gs.mumble_inst.users[data.actor]['name'] not in settings.lobby_users:
                    try:
                        if settings.max_bet >= float(split_data[1]) >= settings.min_bet:
                            settings.lobby_users[gs.mumble_inst.users[data.actor]['name']] = float(split_data[1])
                            gs.gui_service.quick_gui(f"<font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>{gs.mumble_inst.users[data.actor]['name']}</font> has joined the blackjack lobby "
                                                     f"with a <font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>${float(split_data[1]):.2f}</font> bet.",
                                                     text_type='header', box_align='left')
                        else:
                            gs.gui_service.quick_gui(
                                CMD_INVALID_BET,
                                text_type='header',
                                box_align='left', user=gs.mumble_inst.users[data.actor]['name'],
                                ignore_whisper=True)
                    except ValueError:
                        gs.gui_service.quick_gui(
                            CMD_INVALID_JOIN,
                            text_type='header',
                            box_align='left', user=gs.mumble_inst.users[data.actor]['name'],
                            ignore_whisper=True)
            else:
                gs.gui_service.quick_gui(GAME_LOBBY_FULL,
                                         text_type='header', box_align='left', text_align='left',
                                         user=gs.mumble_inst.users[data.actor]['name'])

    def cmd_showhand(self, data):
        if settings.game_started:
            if gs.mumble_inst.users[data.actor]['name'] in settings.game_users.keys():
                hand_str = f"Your hand:<br>{', '.join(card.value for card in settings.game_users[gs.mumble_inst.users[data.actor]['name']].hand.cards)}"
                gs.gui_service.quick_gui(hand_str,
                                         text_type='header', box_align='left', text_align='left',
                                         user=gs.mumble_inst.users[data.actor]['name'])

    def cmd_showplayers(self, data):
        if settings.game_started:
            players_str = f"Players in game:<br>{'<br>'.join(settings.game_users.keys())}"
            gs.gui_service.quick_gui(players_str,
                                     text_type='header', box_align='left', text_align='left',
                                     user=gs.mumble_inst.users[data.actor]['name'])
        elif settings.game_waiting:
            players_str = f"Players waiting in game lobby:<br>{'<br>'.join(list(settings.lobby_users))}"
            gs.gui_service.quick_gui(players_str,
                                     text_type='header', box_align='left', text_align='left',
                                     user=gs.mumble_inst.users[data.actor]['name'])

    def cmd_hit(self, data):
        if settings.game_started:
            if settings.current_player.player == gs.mumble_inst.users[data.actor]['name']:
                blackjack_utility.hit()

    def cmd_stay(self, data):
        if settings.game_started:
            if settings.current_player.player == gs.mumble_inst.users[data.actor]['name']:
                blackjack_utility.stay()

    def cmd_double(self,data):
        if settings.game_started:
            if settings.current_player.player == gs.mumble_inst.users[data.actor]['name']:
                blackjack_utility.double()