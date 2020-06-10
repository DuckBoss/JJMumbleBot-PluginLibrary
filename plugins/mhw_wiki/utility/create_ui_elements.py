from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.helpers import image_helper as ImageHelper
from JJMumbleBot.lib.utils import dir_utils


def create_monster_list(monster_fuzzes):
    content = global_settings.gui_service.make_content(
        f"""Search Results:<br>{'<br>'.join([f'<font color="{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}">[{i}]</font> - {item[0]}' for i, item in enumerate(monster_fuzzes)])}""",
        'header',
        text_align='left'
    )
    return content


def create_monster_title(monster_data_dict):
    content = global_settings.gui_service.make_content(
        f"""<h2>{monster_data_dict['name']}</h2><br>""",
        'header',
        text_color=global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL],
        text_align='center'
    )
    return content


def create_monster_image(monster_data_dict, max_img_size=65536):
    if monster_data_dict['image'] is not None:
        img_string = ImageHelper.format_image(
            f'{monster_data_dict["image"]}',
            'jpg',
            f'{dir_utils.get_perm_med_dir()}/mhw_wiki',
            size_goal=max_img_size,
            max_width=250,
            max_height=250
        )
        content = global_settings.gui_service.make_content(
            f"""{img_string}""",
            'header',
            text_color=global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL],
            text_align='center'
        )
    else:
        content = global_settings.gui_service.make_content(
            f"""Image Unavailable""",
            'header',
            text_color=global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL],
            text_align='center'
        )
    return content


def create_monster_type(monster_data_dict):
    if monster_data_dict['size'] == 'large':
        if int(monster_data_dict['pitfall_trap']) == 0 and int(monster_data_dict['shock_trap']) == 0:
            content = global_settings.gui_service.make_content(
                f"""<font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Type:</font> Elder Dragon""",
                'data',
                text_align='left'
            )
        else:
            content = global_settings.gui_service.make_content(
                f"""<font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Type:</font> {monster_data_dict['size'].title()}""",
                'data',
                text_align='left'
            )
    else:
        content = global_settings.gui_service.make_content(
            f"""<font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Type:</font> {monster_data_dict['size'].title()}""",
            'data',
            text_align='left'
        )
    return content


def create_monster_ailments(monster_data_dict):
    ailments_list = []
    for key in monster_data_dict:
        if 'ailment' in key:
            try:
                if int(monster_data_dict[key]) == 1:
                    ailment_name = key.replace('ailment_', '').title()
                    ailments_list.append(ailment_name)
            except ValueError:
                continue
            except TypeError:
                continue
    content = global_settings.gui_service.make_content(
        f"""<font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Ailments:</font> {', '.join(ailments_list) if len(ailments_list) > 0 else 'None'}""",
        'data',
        text_align='left'
    )
    return content


def create_monster_weaknesses(monster_data_dict):
    weaknesses_list = []
    alt_weaknesses_list = []
    if int(monster_data_dict['has_weakness']) == 0:
        content_weaknesses = global_settings.gui_service.make_content(
            f"""<font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Weaknesses:</font> None""",
            'data',
            text_align='left'
        )
        return content_weaknesses
    for key in monster_data_dict:
        if 'weakness_' in key and monster_data_dict[key] is not None:
            if 'alt_weakness_' in key:
                weakness_name = key.replace('alt_weakness_', '').title()
                weakness = (weakness_name, '\u2605' * int(monster_data_dict[key]))
                alt_weaknesses_list.append(weakness)
            else:
                weakness_name = key.replace('weakness_', '').title()
                weakness = (weakness_name, '\u2605' * int(monster_data_dict[key]))
                weaknesses_list.append(weakness)

    weakness_items = []
    weaknesses_table_text = f'<table style="height: 50%; width:100%;"><tr><th>Weakness Type</th><th>Primary Weakness</th><th>Alt Weakness</th></tr>'
    if len(weaknesses_list) > 0:
        for weakness in weaknesses_list:
            if len(weakness[1]) > 1:
                weakness_item = f'<tr><td style="text-align:center">{weakness[0]}</td><td style="text-align:center"><font color="yellow">({weakness[1]})</font></td><td><td></tr>'
                for alt_weakness in alt_weaknesses_list:
                    if alt_weakness[0] == weakness[0]:
                        if len(alt_weakness[1]) == len(weakness[1]):
                            weakness_item = f'<tr><td style="text-align:center">{weakness[0]}</td><td style="text-align:center"><font color="yellow">({weakness[1]})</font></td><td></td></tr>'
                        else:
                            weakness_item = f'<tr><td style="text-align:center">{weakness[0]}</td><td style="text-align:center"><font color="yellow">({weakness[1]})</font></td><td style="text-align:center"><font color="fuchsia">[{alt_weakness[1]}]</font></td></tr>'
                        if len(alt_weakness[1]) == 0:
                            weakness_item = f'<tr><td style="text-align:center">{weakness[0]}</td><td style="text-align:center"><font color="yellow">({weakness[1]})</font></td><td style="text-align:center"><font color="fuchsia">[Immune]</font></td></tr>'
                weakness_items.append(weakness_item)
            else:
                for alt_weakness in alt_weaknesses_list:
                    if alt_weakness[0] == weakness[0]:
                        if len(alt_weakness) > 1:
                            if len(alt_weakness[1]) > 0:
                                weakness_item = f'<tr><td style="text-align:center">{weakness[0]}</td><td style="text-align:center"><font color="yellow">(Immune)</font></td><td style="text-align:center"><font color="fuchsia">[{alt_weakness[1]}]</font></td></tr>'
                            else:
                                weakness_item = f'<tr><td style="text-align:center">{weakness[0]}</td><td style="text-align:center"><font color="yellow">(Immune)</font></td></tr>'
                            weakness_items.append(weakness_item)
    weaknesses_table_text += ''.join(x for x in weakness_items) + '</table>'
    # print(weaknesses_table_text)
    content_weaknesses = global_settings.gui_service.make_content(
        f"""<font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Weaknesses:</font><br>{weaknesses_table_text}""",
        'data',
        text_align='left'
    )
    return content_weaknesses


def create_monster_locations(monster_data_dict):
    location_content = global_settings.gui_service.make_content(
        f"""<font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Locations:</font> {', '.join(monster_data_dict['locations']) if len(monster_data_dict['locations']) > 0 else 'Unavailable'}""",
        'data',
        text_align='left'
    )
    return location_content


def create_monster_link(monster_data_dict):
    location_content = global_settings.gui_service.make_content(
        f"""<font color='{global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>Wiki Link:</font> {monster_data_dict['link']}""",
        'data',
        text_align='left'
    )
    return location_content
