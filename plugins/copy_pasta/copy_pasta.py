from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.resources.strings import *


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def get_metadata(self):
        return self.metadata

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "shrug":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            GS.gui_service.quick_gui("¯\_(ツ)_/¯", text_type='header', box_align='left')
            return
        elif command == "lenny":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            GS.gui_service.quick_gui("( ͡° ͜ʖ ͡°)", text_type='header', box_align='left')
            return
        elif command == "fliptable":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            GS.gui_service.quick_gui("(╯°□°）╯︵ ┻━┻", text_type='header', box_align='left')
            return
