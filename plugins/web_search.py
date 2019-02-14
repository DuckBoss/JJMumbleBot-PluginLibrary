from plugin_template import PluginBase
import utils
from googlesearch import search
import requests
import time

class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> Web_Search Plugin Help <font color='red'>#####</font></b><br> \
                        All commands can be run by typing it in the channel or privately messaging DuckBot.<br>\
                        <b>!google 'search_term'</b>: Returns google search results for the search term."

    headers = {'headers': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    def __init__(self):
        super().__init__()

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "google":
            parameter = message_parse[1]
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       self.google_search(parameter))
            return

    def google_search(self, search_term):
        final_result = "<br><font color='red'>Google Search Results:</font> <font color='cyan'>%s</font><br>" % search_term
        counter = 0
        for url in search(search_term, stop=5, num=5, only_standard=False, user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'):
            title = self.google_scrape(url)
            final_result += "<font color='cyan'>[%d]:</font> <font color='yellow'>%s</font><br><a href='%s'>%s</a><br>" % (counter, title, url, url)
            counter += 1
            time.sleep(0.2)
        return final_result

    def google_scrape(self, url):
        n = requests.get(url, headers=self.headers)
        al = n.text
        return al[al.find('<title>')+7: al.find('</title>')]

    def plugin_test(self):
        print("Web_Search Plugin self-test callback.")

    def quit(self):
        print("Exiting Web_Search Plugin...")

    def help(self):
        return self.help_data
