from plugin_template import PluginBase
import utils
import requests


class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> LMGTFY Plugin Help <font color='red'>#####</font></b><br> \
                    All commands can be run by typing it in the channel or privately messaging DuckBot.<br>\
                    <b>!lmgtfy 'message'</b>: Let me google that for you..."

    def __init__(self):
        print("LMGTFY Plugin Initialized.")
        super().__init__()

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "lmgtfy":
            parameter = message_parse[1]
            results = self.lmgtfy(parameter)
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                                     "<a href='%s'>%s</a>" % (results, results))

    def lmgtfy(self, query):
        lmgtfy_url = 'http://lmgtfy.com/?q=' + '+'.join([word.replace(" ", "+") for word in query.split()])
        payload = {'format': 'json', 'url': lmgtfy_url}
        r = requests.get('http://is.gd/create.php', params=payload)
        return r.json()['shorturl']

    @staticmethod
    def plugin_test():
        print("LMGTFY Plugin self-test callback.")

    def quit(self):
        print("Exiting LMGTFY Plugin...")

    def help(self):
        return self.help_data