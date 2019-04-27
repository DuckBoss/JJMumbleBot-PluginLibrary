from templates.plugin_template import PluginBase
from helpers.global_access import debug_print, reg_print
from helpers.global_access import GlobalMods as GM
import privileges as pv


class Plugin(PluginBase):
    help_data = "All commands can be run by typing it in the channel or privately messaging DuckBot.<br>\
                <b>!shrug</b>: Displays the shrug emoji.<br>\
                <b>!lenny</b>: Displays the lenny face emoji.<br>\
                <b>!fliptable</b>: Displays the flip table emoji."
    plugin_version = "2.0.0"
    priv_path = "copy_pasta/copy_pasta_privileges.csv"

    def __init__(self):
        debug_print("Copy_Pasta Plugin Initialized.")
        super().__init__()

    def process_command(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "shrug":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.quick_gui("¯\_(ツ)_/¯", text_type='header', box_align='left')
            return
        elif command == "lenny":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.quick_gui("( ͡° ͜ʖ ͡°)", text_type='header', box_align='left')
            return
        elif command == "fliptable":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.quick_gui("(╯°□°）╯︵ ┻━┻", text_type='header', box_align='left')
            return

    def plugin_test(self):
        debug_print("Copy_Pasta Plugin self-test callback.")

    def quit(self):
        debug_print("Exiting Copy_Pasta Plugin")

    def is_audio_plugin(self):
        return False

    def help(self):
        return self.help_data

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path

