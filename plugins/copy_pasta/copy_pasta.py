import utils
from templates.plugin_template import PluginBase
from helpers.global_access import debug_print, reg_print
import privileges as pv


class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> Copy_Pasta Plugin Help <font color='red'>#####</font></b><br> \
                All commands can be run by typing it in the channel or privately messaging DuckBot.<br>\
                <b>!shrug</b>: Displays the shrug emoji.<br>\
                <b>!lenny</b>: Displays the lenny face emoji.<br>\
                <b>!fliptable</b>: Displays the flip table emoji."
    plugin_version = "1.6.0"
    priv_path = "copy_pasta/copy_pasta_privileges.csv"

    def __init__(self):
        debug_print("Copy_Pasta Plugin Initialized.")
        super().__init__()

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "shrug":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                                     "¯\_(ツ)_/¯")
            return
        elif command == "lenny":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                                     "( ͡° ͜ʖ ͡°)")
            return
        elif command == "fliptable":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                                     "(╯°□°）╯︵ ┻━┻")
            return

    @staticmethod
    def plugin_test():
        debug_print("Copy_Pasta Plugin self-test callback.")

    def quit(self):
        debug_print("Exiting Copy_Pasta Plugin")

    def help(self):
        return self.help_data

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path

