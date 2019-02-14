import utils
from plugin_template import PluginBase


class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> Copy_Pasta Plugin Help <font color='red'>#####</font></b><br> \
                All commands can be run by typing it in the channel or privately messaging DuckBot.<br>\
                <b>!shrug</b>: Displays the shrug emoji.<br>\
                <b>!lenny</b>: Displays the lenny face emoji.<br>\
                <b>!fliptable</b>: Displays the flip table emoji."

    def __init__(self):
        print("Copy_Pasta Plugin Initialized.")
        super().__init__()

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "shrug":
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                                     "¯\_(ツ)_/¯")
            return
        elif command == "lenny":
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                                     "( ͡° ͜ʖ ͡°)")
            return
        elif command == "fliptable":
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                                     "(╯°□°）╯︵ ┻━┻")
            return

    @staticmethod
    def plugin_test():
        print("Copy_Pasta Plugin self-test callback.")

    def quit(self):
        print("Exiting Copy_Pasta Plugin")

    def help(self):
        return self.help_data

