from templates.plugin_template import PluginBase
from helpers.global_access import debug_print
from helpers.global_access import GlobalMods as GM
import requests
import privileges as pv


class Plugin(PluginBase):
    help_data = "All commands can be run by typing it in the channel or privately messaging DuckBot.<br>\
                    <b>!lmgtfy 'message'</b>: Let me google that for you..."
    plugin_version = "2.0.0"
    priv_path = "lmgtfy/lmgtfy_privileges.csv"

    def __init__(self):
        debug_print("LMGTFY Plugin Initialized.")
        super().__init__()

    def process_command(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "lmgtfy":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            parameter = message_parse[1]
            results = self.lmgtfy(parameter)
            GM.gui.quick_gui(f"<a href='{results}'>{results}</a>", text_type='header', box_align='left')

    def lmgtfy(self, query):
        lmgtfy_url = 'http://lmgtfy.com/?q=' + '+'.join([word.replace(" ", "+") for word in query.split()])
        payload = {'format': 'json', 'url': lmgtfy_url}
        r = requests.get('http://is.gd/create.php', params=payload)
        return r.json()['shorturl']

    def plugin_test(self):
        debug_print("LMGTFY Plugin self-test callback.")

    def is_audio_plugin(self):
        return False

    def quit(self):
        debug_print("Exiting LMGTFY Plugin...")

    def help(self):
        return self.help_data

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path
