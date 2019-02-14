import utils
from plugin_template import PluginBase
import random
from datetime import datetime


class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> Oblivion Character Creator Plugin Help <font color='red'>#####</font></b><br> \
                All commands can be run by typing it in the channel or privately messaging DuckBot.<br>\
                <b>!oblivion</b>: Generates a custom random oblivion character and messages it to the user.<br>\
                <b>!oblivion_echo</b>: Generates a custom random oblivion character and messages it to the channel.<br>"

    spec_list = ['Combat', 'Magic', 'Stealth']
    attr_list = ['Strength', 'Intelligence', 'Willpower', 'Agility', 'Speed', 'Endurance', 'Personality', 'Luck']
    skill_list = ['Blade', 'Blunt', 'Hand To Hand', 'Armorer', 'Block', 'Heavy Armor', 'Athletics', 'Acrobatics',
                  'Light Armor', 'Security', 'Sneak', 'Marksman', 'Mercantile', 'Speechcraft', 'Illusion', 'Alchemy',
                  'Conjuration', 'Mysticism', 'Alteration', 'Destruction', 'Restoration']

    def __init__(self):
        print("Oblivion Character Creator Plugin Initialized.")
        super().__init__()

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "oblivion":
            self.randomize()
            speciality = self.choose_spec()
            attributes = self.choose_attrs()
            skills = self.choose_skills()

            ret_text = "<font color='cyan'>Specialty:</font><br><font color='yellow'>{spec}</font><br>" \
                       "<font color='cyan'>Attributes:</font><br><font color='yellow'>{attr_1}<br>{attr_2}</font><br>" \
                       "<font color='cyan'>Skills:</font><br><font color='yellow'>{skill_1}<br>{skill_2}<br>{skill_3}<br>{skill_4}" \
                       "<br>{skill_5}<br>{skill_6}<br>{skill_7}</font>".format(spec=speciality, attr_1=attributes[0], attr_2=attributes[1], skill_1=skills[0], skill_2=skills[1], skill_3=skills[2], skill_4=skills[3], skill_5=skills[4], skill_6=skills[5], skill_7=skills[6])

            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "Oblivion character generated for: {actor}".format(actor=mumble.users[text.actor]['name']))

            utils.msg(mumble, mumble.users[text.actor]['name'],
                       "<br><font color='red'>Character Generated -</font><br>{ret}".format(ret=ret_text))

            return

        if command == "oblivion_echo":
            self.randomize()
            speciality = self.choose_spec()
            attributes = self.choose_attrs()
            skills = self.choose_skills()

            ret_text = "<font color='cyan'>Specialty:</font><br><font color='yellow'>{spec}</font><br>" \
                       "<font color='cyan'>Attributes:</font><br><font color='yellow'>{attr_1}<br>{attr_2}</font><br>" \
                       "<font color='cyan'>Skills:</font><br><font color='yellow'>{skill_1}<br>{skill_2}<br>{skill_3}<br>{skill_4}" \
                       "<br>{skill_5}<br>{skill_6}<br>{skill_7}</font>".format(spec=speciality, attr_1=attributes[0], attr_2=attributes[1], skill_1=skills[0], skill_2=skills[1], skill_3=skills[2], skill_4=skills[3], skill_5=skills[4], skill_6=skills[5], skill_7=skills[6])

            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "Oblivion character generated for: {actor}".format(actor=mumble.users[text.actor]['name']))

            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "<br><font color='red'>Character Generated -</font><br>{ret}".format(ret=ret_text))

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

    @staticmethod
    def plugin_test():
        print("Oblivion Character Creator Plugin self-test callback.")

    def quit(self):
        print("Exiting Oblivion Character Creator Plugin")

    def help(self):
        return self.help_data

