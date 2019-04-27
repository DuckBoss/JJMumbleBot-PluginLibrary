from templates.plugin_template import PluginBase
from helpers.global_access import debug_print
from helpers.global_access import GlobalMods as GM
import random
from datetime import datetime
import privileges as pv


class Plugin(PluginBase):
    help_data = "All commands can be run by typing it in the channel or privately messaging DuckBot.<br>\
                <b>!oblivion</b>: Generates a custom random oblivion character and messages it to the user.<br>\
                <b>!oblivion_echo</b>: Generates a custom random oblivion character and messages it to the channel.<br>"

    spec_list = ['Combat', 'Magic', 'Stealth']
    attr_list = ['Strength', 'Intelligence', 'Willpower', 'Agility', 'Speed', 'Endurance', 'Personality', 'Luck']
    skill_list = ['Blade', 'Blunt', 'Hand To Hand', 'Armorer', 'Block', 'Heavy Armor', 'Athletics', 'Acrobatics',
                  'Light Armor', 'Security', 'Sneak', 'Marksman', 'Mercantile', 'Speechcraft', 'Illusion', 'Alchemy',
                  'Conjuration', 'Mysticism', 'Alteration', 'Destruction', 'Restoration']

    plugin_version = "2.0.0"
    priv_path = "oblivion_creator/oblivion_creator_privileges.csv"

    def __init__(self):
        debug_print("Oblivion Character Creator Plugin Initialized.")
        super().__init__()

    def process_command(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "oblivion":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            self.randomize()
            speciality = self.choose_spec()
            attributes = self.choose_attrs()
            skills = self.choose_skills()

            ret_text = f"<font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>Specialty:</font><br>{speciality}<br>" \
                       f"<font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>Attributes:</font><br>{attributes[0]}<br>{attributes[1]}<br>" \
                       f"<font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>Skills:</font><br>{skills[0]}<br>{skills[1]}<br>{skills[2]}<br>{skills[3]}" \
                       f"<br>{skills[4]}<br>{skills[5]}<br>{skills[6]}"

            GM.gui.quick_gui(f"Oblivion character generated for: {GM.mumble.users[text.actor]['name']}", text_type='header', box_align='left')

            GM.gui.quick_gui(f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>Oblivion Character Generated:</font><br>{ret_text}", text_type='header', box_align='left', user=GM.mumble.users[text.actor]['name'])
            return

        if command == "oblivion_echo":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            self.randomize()
            speciality = self.choose_spec()
            attributes = self.choose_attrs()
            skills = self.choose_skills()

            ret_text = f"<font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>Specialty:</font><br>{speciality}<br>" \
                       f"<font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>Attributes:</font><br>{attributes[0]}<br>{attributes[1]}<br>" \
                       f"<font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>Skills:</font><br>{skills[0]}<br>{skills[1]}<br>{skills[2]}<br>{skills[3]}" \
                       f"<br>{skills[4]}<br>{skills[5]}<br>{skills[6]}"

            GM.gui.quick_gui(f"Oblivion character generated for: {GM.mumble.users[text.actor]['name']}", text_type='header', box_align='left')

            GM.gui.quick_gui(f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>Oblivion Character Generated:</font><br>{ret_text}", text_type='header', box_align='left')
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

    def plugin_test(self):
        debug_print("Oblivion Character Creator Plugin self-test callback.")

    def quit(self):
        debug_print("Exiting Oblivion Character Creator Plugin")

    def help(self):
        return self.help_data

    def is_audio_plugin(self):
        return False

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path
