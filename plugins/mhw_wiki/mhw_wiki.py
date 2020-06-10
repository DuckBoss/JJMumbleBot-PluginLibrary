from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib import privileges
from JJMumbleBot.plugins.extensions.mhw_wiki.resources.strings import *
from JJMumbleBot.plugins.extensions.mhw_wiki.utility.mhw_utility import find_monster, define_all_monsters, search_monsters
from JJMumbleBot.plugins.extensions.mhw_wiki.utility.create_ui_elements import create_monster_list, create_monster_title, create_monster_image, create_monster_type, create_monster_ailments, create_monster_weaknesses, create_monster_locations, create_monster_link
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.utils.runtime_utils import get_my_channel
import sqlite3


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from os import path, makedirs
        from json import loads
        import shutil
        import errno
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        # Copy over monster_images directory to the permanent media directory.
        try:
            if not path.exists(path.join(dir_utils.get_perm_med_dir(), 'mhw_wiki')):
                makedirs(path.join(dir_utils.get_perm_med_dir(), 'mhw_wiki'))
        except FileExistsError:
            pass
        try:
            shutil.copytree(path.join(path.dirname(__file__), 'resources/monster_images'), path.join(dir_utils.get_perm_med_dir(), 'mhw_wiki'))
        except OSError as e:
            if e.errno == errno.EEXIST:
                from distutils.dir_util import copy_tree
                copy_tree(path.join(path.dirname(__file__), 'resources/monster_images'), path.join(dir_utils.get_perm_med_dir(), 'mhw_wiki'))
        # Initialize database definitions
        self.mhw_db = sqlite3.connect(path.join(path.dirname(__file__), 'resources/mhw.db'))
        self.img_path = path.join(path.dirname(__file__), 'resources/monster_images')
        self.mhw_cursor = self.mhw_db.cursor()
        self.monster_definitions = define_all_monsters(self.mhw_cursor, self.img_path)
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

        if command == "mhw_search":
            search_term = message_parse[1].strip()

            # Retrieve the monster data dictionary and display an error if a valid monster isn't found.
            rprint("Retrieving monster information...", origin=L_COMMAND)
            monster_fuzzes = search_monsters(search_term, search_threshold=70)
            print(monster_fuzzes)
            if monster_fuzzes is None or len(monster_fuzzes) == 0:
                global_settings.gui_service.quick_gui(
                    f"There were no results for the search query: {search_term}",
                    text_type='header', box_align='left')
                return

            # Construct the UI for the monster information.
            global_settings.gui_service.open_box(align='center')
            rprint("Formatting MHW wiki information into pgui...", origin=L_COMMAND)
            # Append monster search results.
            monster_results = create_monster_list(monster_fuzzes)
            global_settings.gui_service.append_row(monster_results)
            # Close the UI.
            global_settings.gui_service.close_box()
            global_settings.gui_service.display_box(channel=get_my_channel(), ignore_whisper=True)

        if command == "mhw":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return

            if len(message_parse) < 2:
                return
            search_term = message_parse[1].strip()

            # Retrieve the monster data dictionary and display an error if a valid monster isn't found.
            rprint("Retrieving monster information...", origin=L_COMMAND)
            monster_data_dict = find_monster(self.monster_definitions, monster_name=search_term, search_threshold=70)
            if monster_data_dict is None:
                global_settings.gui_service.quick_gui(
                    f"This monster was not found in the monster name dictionary: {search_term}",
                    text_type='header', box_align='left')
                return

            # Construct the UI for the monster information.
            global_settings.gui_service.open_box(align='center')
            rprint("Formatting MHW wiki information into pgui...", origin=L_COMMAND)

            # Part 1 - UI Creation: Create the monster title
            monster_title = create_monster_title(monster_data_dict)
            global_settings.gui_service.append_row(monster_title)

            # Part 2 - UI Creation: Create the monster image
            if self.metadata.getboolean(C_PLUGIN_SETTINGS, P_USE_IMAGE, fallback=False):
                monster_image = create_monster_image(monster_data_dict, int(self.metadata[C_PLUGIN_SETTINGS][P_IMG_MAX_SIZE]))
                global_settings.gui_service.append_row(monster_image)

            # Part 3 - UI Creation: Create the monster type
            monster_type = create_monster_type(monster_data_dict)
            global_settings.gui_service.append_row(monster_type)

            # Part 4 - UI Creation: Create the monster ailments
            monster_ailments = create_monster_ailments(monster_data_dict)
            global_settings.gui_service.append_row(monster_ailments)

            # Part 5 - UI Creation: Create the monster weaknesses
            monster_weaknesses = create_monster_weaknesses(monster_data_dict)
            global_settings.gui_service.append_row(monster_weaknesses)
            # global_settings.gui_service.append_row(monster_weaknesses[1])

            # Part 6 - UI Creation: Create the monster location
            monster_locations = create_monster_locations(monster_data_dict)
            global_settings.gui_service.append_row(monster_locations)

            # Part 7 - UI Creation: Create the monster wiki link
            # Add the wiki link of the monster to the monster data dictionary.
            monster_link_format = monster_data_dict["name"].replace(" ", "+")
            monster_data_dict['link'] = f'<a href="https://monsterhunterworld.wiki.fextralife.com/{monster_link_format}">{monster_data_dict["name"]}</a>'
            monster_link = create_monster_link(monster_data_dict)
            global_settings.gui_service.append_row(monster_link)

            rprint("MHW wiki PGUI complete.", origin=L_COMMAND)
            # Close the UI.
            global_settings.gui_service.close_box()
            global_settings.gui_service.display_box(channel=get_my_channel(), ignore_whisper=True)
