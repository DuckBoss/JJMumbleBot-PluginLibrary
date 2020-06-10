from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.resources.strings import *
import random
from datetime import datetime


class Plugin(PluginBase):
    spec_list = ['Combat', 'Magic', 'Stealth']
    attr_list = ['Strength', 'Intelligence', 'Willpower', 'Agility', 'Speed', 'Endurance', 'Personality', 'Luck']
    skill_list = ['Blade', 'Blunt', 'Hand To Hand', 'Armorer', 'Block', 'Heavy Armor', 'Athletics', 'Acrobatics',
                  'Light Armor', 'Security', 'Sneak', 'Marksman', 'Mercantile', 'Speechcraft', 'Illusion', 'Alchemy',
                  'Conjuration', 'Mysticism', 'Alteration', 'Destruction', 'Restoration']

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

        if command == "oblivion":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            self.randomize()
            speciality = self.choose_spec()
            attributes = self.choose_attrs()
            skills = self.choose_skills()

            ret_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Specialty:</font><br>{speciality}<br>" \
                       f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Attributes:</font><br>{attributes[0]}<br>{attributes[1]}<br>" \
                       f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Skills:</font><br>{skills[0]}<br>{skills[1]}<br>{skills[2]}<br>{skills[3]}" \
                       f"<br>{skills[4]}<br>{skills[5]}<br>{skills[6]}"

            GS.gui_service.quick_gui(f"Oblivion character generated for: {GS.mumble_inst.users[text.actor]['name']}", text_type='header', box_align='left')

            GS.gui_service.quick_gui(f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Oblivion Character Generated:</font><br>{ret_text}", text_type='header', box_align='left', user=GS.mumble_inst.users[text.actor]['name'])
            return

        if command == "oblivion_echo":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            self.randomize()
            speciality = self.choose_spec()
            attributes = self.choose_attrs()
            skills = self.choose_skills()

            ret_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Specialty:</font><br>{speciality}<br>" \
                       f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Attributes:</font><br>{attributes[0]}<br>{attributes[1]}<br>" \
                       f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Skills:</font><br>{skills[0]}<br>{skills[1]}<br>{skills[2]}<br>{skills[3]}" \
                       f"<br>{skills[4]}<br>{skills[5]}<br>{skills[6]}"

            GS.gui_service.quick_gui(f"Oblivion character generated for: {GS.mumble_inst.users[text.actor]['name']}", text_type='header', box_align='left')

            GS.gui_service.quick_gui(f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Oblivion Character Generated:</font><br>{ret_text}", text_type='header', box_align='left')
            return

    def randomize(self):
        random.seed(datetime.now())
        random.shuffle(self.spec_list)
        random.seed(datetime.now())
        random.shuffle(self.attr_list)
        random.seed(datetime.now())
        random.shuffle(self.skill_list)

    def choose_spec(self):
        return random.choice(self.spec_list)

    def choose_attrs(self):
        attr_list_copy = self.attr_list.copy()
        attr_ret = []
        for i in range(2):
            cur_attr = random.choice(attr_list_copy)
            attr_list_copy.remove(cur_attr)
            attr_ret.append(cur_attr)
            random.seed(datetime.now())
        return attr_ret

    def choose_skills(self):
        skills_list_copy = self.skill_list.copy()
        skills_ret = []
        for i in range(7):
            cur_attr = random.choice(skills_list_copy)
            skills_list_copy.remove(cur_attr)
            skills_ret.append(cur_attr)
            random.seed(datetime.now())
        return skills_ret
