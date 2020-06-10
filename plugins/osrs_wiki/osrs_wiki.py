from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib import privileges
from JJMumbleBot.plugins.extensions.osrs_wiki.resources.strings import *
from mediawiki import MediaWiki
from mediawiki import exceptions
from bs4 import BeautifulSoup
import urllib.request
import json


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        self.osrs_wiki_url = self.metadata[C_PLUGIN_SET][P_WIKI_URL]
        self.osrs_user_agent = self.metadata[C_PLUGIN_SET][P_USER_AGENT]
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")
        try:
            self.osrs_wiki = MediaWiki(url=self.osrs_wiki_url, user_agent=self.osrs_user_agent)
        except Exception:
            rprint(f"{self.plugin_name} Plugin could not be initialized.")

    def quit(self):
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def get_metadata(self):
        return self.metadata

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "price":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if self.osrs_wiki is None:
                self.osrs_wiki = MediaWiki(url=self.metadata[C_PLUGIN_SETTINGS][P_WIKI_URL], user_agent=self.metadata[C_PLUGIN_SETTINGS][P_USER_AGENT])

            parameter = message_parse[1]
            search_criteria = self.manage_search_criteria(parameter)
            all_item_data = self.pull_json(search_criteria)
            if all_item_data is not None:
                item_data_formatted = "<br><font color='{}'>Item:</font> {}<br>Avg. Price: {:,} coins.".format(global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL], all_item_data['name'].title(), all_item_data['overall_average'])
                item_data_formatted += "<br><font color='{}'>Buy Avg. Price:</font> {:,} coins.".format(global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL], all_item_data['buy_average'])
                item_data_formatted += "<br><font color='{}'>Sell Avg. Price:</font> {:,} coins.".format(global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL], all_item_data['sell_average'])

                global_settings.gui_service.quick_gui(item_data_formatted, text_type='header', box_align='left')
            else:
                global_settings.gui_service.quick_gui(f"Could not find '{search_criteria}' on the grand exchange.", text_type='header', box_align='left')

        elif command == "osrs":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if self.osrs_wiki is None:
                self.osrs_wiki = MediaWiki(url=self.metadata[C_PLUGIN_SETTINGS][P_WIKI_URL], user_agent=self.metadata[C_PLUGIN_SETTINGS][P_USER_AGENT])

            parameter = message_parse[1]
            global_settings.gui_service.quick_gui(f"Searching the OSRS Wiki for: {parameter}", text_type='header', box_align='left')
            search_results = self.osrs_wiki.opensearch(parameter)
            formatted_results = self.get_choices(search_results)

            if formatted_results is None:
                global_settings.gui_service.quick_gui("OSRS Wiki Results:<br>No search results found.", text_type='header', box_align='left')
                return
            global_settings.gui_service.quick_gui(f"OSRS Wiki Results:<br>{formatted_results}\n", text_type='header', box_align='left')

        elif command == "quest":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if self.osrs_wiki is None:
                self.osrs_wiki = MediaWiki(url=self.metadata[C_PLUGIN_SETTINGS][P_WIKI_URL], user_agent=self.metadata[C_PLUGIN_SETTINGS][P_USER_AGENT])

            parameter = message_parse[1]
            global_settings.gui_service.quick_gui(f"Searching the OSRS Wiki for: {parameter}", text_type='header', box_align='left')

            try:
                page = self.osrs_wiki.page(parameter)
            except exceptions.PageError:
                global_settings.gui_service.quick_gui("OSRS Wiki Results:<br>No search results found.", text_type='header', box_align='left')
                return

            if "Quests" not in page.categories and page is not None:
                global_settings.gui_service.quick_gui("OSRS Wiki Results:<br>No search results found.", text_type='header', box_align='left')
                return

            soup = BeautifulSoup(page.html, 'html.parser')
            tds = soup.find_all('td', class_="questdetails-info")
            final_text = f"<br><u><font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>{page.title} Quest Summary</font></u><br><a href='{page.url}'>{page.url}</a>"
            for i, item in enumerate(tds):
                f_text = ""

                if i == 0:
                    f_text = "<br><font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Start Point:</font><br>"
                elif i == 1:
                    f_text = "<br><font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Difficulty:</font><br>"
                elif i == 2:
                    f_text = "<br><font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Description:</font><br>"
                elif i == 3:
                    f_text = "<br><font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Length:</font><br>"
                elif i == 4:
                    f_text = "<br><font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Requirements:</font><br>"
                elif i == 5:
                    f_text = "<br><font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Items Required:</font><br>"
                elif i == 6:
                    f_text = "<br><font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Enemies To Defeat:</font><br>"

                counter = 0
                if i == 4 or i == 6:
                    uls = item.find_all('ul')
                    if uls is not None:
                        for ul in uls:
                            lis = ul.find_all('li')
                            for li in lis:
                                f_text += f"<font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>-- </font>{li.text}<br>"
                    else:
                        f_text += "UNAVAILABLE"
                elif i == 5:
                    uls = item.find_all('ul')
                    if uls is not None:
                        for ul in item.find_all('ul'):
                            lis = ul.find_all('li')
                            for li in lis:
                                f_text += f"<font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>-- </font>{li.text}<br>"

                            if counter == 0:
                                f_text += f"<br><font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Recommended Items:</font><br>"
                            counter += 1
                    else:
                        f_text += "UNAVAILABLE"
                else:
                    f_text += tds[i].text

                final_text += f_text
            global_settings.gui_service.quick_gui(final_text, text_type='header', box_align='left')

    def get_choices(self, search_results):
        list_urls = "<br>"
        if search_results:
            for i, item in enumerate(search_results):
                completed_url = item[2]
                list_urls += f"<font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font>: <a href='{completed_url}'>[{completed_url}]</a><br>"
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
        with urllib.request.urlopen(self.metadata[C_PLUGIN_SETTINGS][P_MAIN_URL]) as url:
            json_data = json.loads(url.read().decode('utf-8').lower())
            for section in json_data:
                json_item = json_data[section]
                if json_item.get('name') == search_criteria or json_item.get('id') == search_criteria:
                    return_item = json_item
        return return_item
