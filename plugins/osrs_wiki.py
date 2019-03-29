from mediawiki import MediaWiki
from mediawiki import exceptions
from templates.plugin_template import PluginBase
import utils
from bs4 import BeautifulSoup
import urllib.request
import json


class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> Osrs_Wiki Plugin Help <font color='red'>#####</font></b><br> \
                    All commands can be run by typing it in the channel or privately messaging DuckBot.<br>\
                    <b>!osrs 'message'</b>: Searches the osrs wiki.<br>\
                    <b>!quest 'quest_name'</b>: Searches the osrs wiki for quest details.<br>\
                    <b>!price 'item_name'</b>: Searches the rsbuddy exchange for pricing information."

    osrs_user_agent = 'DuckBot_User_Agent'
    osrs_wiki_url = 'https://oldschool.runescape.wiki/api.php'
    osrs_wiki = None

    json_url = "https://rsbuddy.com/exchange/summary.json"
    json_url2 = "https://api.rsbuddy.com/grandExchange?a=guidePrice&i="

    plugin_version = "1.0.1"

    def __init__(self):
        print("Osrs_Wiki Plugin Initialized.")
        super().__init__()
        try:
            self.osrs_wiki = MediaWiki(url=self.osrs_wiki_url, user_agent=self.osrs_user_agent)
        except Exception:
            print("Osrs_Wiki Plugin could not be initialized.")

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "price":
            if self.osrs_wiki is None:
                self.osrs_wiki = MediaWiki(url=self.osrs_wiki_url, user_agent=self.osrs_user_agent)

            parameter = message_parse[1]
            if parameter == "justin":
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "I'm sorry, but this is fucking worthless.")
                return

            search_criteria = self.manage_search_criteria(parameter)
            all_item_data = self.pull_json(search_criteria)
            if all_item_data is not None:
                item_data_formatted = "<br><font color='red'>Item:</font> {}<br><font color='cyan'>Avg. Price:</font> <font color='yellow'>{:,} coins.</font>".format(all_item_data['name'].title(), all_item_data['overall_average'])
                item_data_formatted += "<br><font color='cyan'>Buy Avg. Price:</font> <font color='yellow'>{:,} coins.</font>".format(all_item_data['buy_average'])
                item_data_formatted += "<br><font color='cyan'>Sell Avg. Price:</font> <font color='yellow'>{:,} coins.</font>".format(all_item_data['sell_average'])

                print(all_item_data)
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           item_data_formatted)
            else:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Could not find '%s' on the grand exchange." % search_criteria)
            return

        elif command == "osrs":
            if self.osrs_wiki is None:
                self.osrs_wiki = MediaWiki(url=self.osrs_wiki_url, user_agent=self.osrs_user_agent)

            parameter = message_parse[1]
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "Searching the OSRS Wiki for: %s" % parameter)
            search_results = self.osrs_wiki.opensearch(parameter)
            formatted_results = self.get_choices(search_results)

            if formatted_results is None:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "OSRS Wiki Results:\nNo search results found.")
                return
            else:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "OSRS Wiki Results:\n%s\n" % formatted_results)
                return

        elif command == "quest":
            if self.osrs_wiki is None:
                self.osrs_wiki = MediaWiki(url=self.osrs_wiki_url, user_agent=self.osrs_user_agent)

            parameter = message_parse[1]
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "Searching the OSRS Wiki for: %s" % parameter)

            try:
                page = self.osrs_wiki.page(parameter)
            except exceptions.PageError:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "OSRS Wiki Results:\nNo search results found.")
                return

            if "Quests" not in page.categories and page is not None:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "OSRS Wiki Results:\nNo search results found.")
                return

            soup = BeautifulSoup(page.html, 'html.parser')
            tds = soup.find_all('td', class_="questdetails-info")
            final_text = "<br><u><font color='cyan'>%s Quest Summary</font></u><br>" \
                         "<a href='%s'>%s</a>" % (page.title, page.url, page.url)
            for i in range(len(tds)):
                f_text = ""

                if i == 0:
                    f_text = "<br><font color='red'>Start Point:</font><br>"
                elif i == 1:
                    f_text = "<br><font color='red'>Difficulty:</font><br>"
                elif i == 2:
                    f_text = "<br><font color='red'>Description:</font><br>"
                elif i == 3:
                    f_text = "<br><font color='red'>Length:</font><br>"
                elif i == 4:
                    f_text = "<br><font color='red'>Requirements:</font><br>"
                elif i == 5:
                    f_text = "<br><font color='red'>Items Required:</font><br>"
                elif i == 6:
                    f_text = "<br><font color='red'>Enemies To Defeat:</font><br>"

                counter = 0
                if i == 4 or i == 6:
                    uls = tds[i].find_all('ul')
                    if uls is not None:
                        for ul in uls:
                            lis = ul.find_all('li')
                            for li in lis:
                                f_text += "<font color='cyan'>-- </font>"+li.text+"<br>"
                    else:
                        f_text += "UNAVAILABLE"
                elif i == 5:
                    uls = tds[i].find_all('ul')
                    if uls is not None:
                        for ul in tds[i].find_all('ul'):
                            lis = ul.find_all('li')
                            for li in lis:
                                f_text += "<font color='cyan'>-- </font>"+li.text+"<br>"

                            if counter == 0:
                                f_text += "<br><font color='red'>Recommended Items:</font><br>"
                            counter += 1
                    else:
                        f_text += "UNAVAILABLE"
                else:
                    f_text += tds[i].text

                final_text += f_text
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "%s" % final_text)
            return

    def get_choices(self, search_results):
        list_urls = "<br>"
        if len(search_results) > 0:
            for i in range(len(search_results)):
                completed_url = search_results[i][2]
                list_urls += "<font color='cyan'>[%d]</font>: <a href='%s'>[%s]</a><br>" % (i, completed_url, completed_url)
        else:
            return None
        return list_urls

    def manage_search_criteria(self, search_criteria):
        try:
            return int(search_criteria)
        except ValueError:
            return search_criteria.lower()

    def pull_json(self, search_criteria):
        return_item = None
        with urllib.request.urlopen(self.json_url) as url:
            json_data = json.loads(url.read().decode('utf-8').lower())
            for section in json_data:
                json_item = json_data[section]
                if json_item.get('name') == search_criteria or json_item.get('id') == search_criteria:
                    return_item = json_item
        return return_item

    def plugin_test(self):
        print("Osrs_Wiki Plugin self-test callback.")

    def quit(self):
        print("Exiting Osrs_Wiki Plugin")

    def help(self):
        return self.help_data

    def get_plugin_version(self):
        return self.plugin_version
