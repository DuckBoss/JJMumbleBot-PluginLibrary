from JJMumbleBot.plugins.extensions.mhw_wiki.utility.custom_typings import MonsterList,  MonsterDict
import JJMumbleBot.plugins.extensions.mhw_wiki.utility.fuzzy_search as fuzzy_search
from os import listdir


def find_monster(monster_list, monster_id=None, monster_name=None, search_threshold=70) -> MonsterDict:
    matched_monsters = []
    if monster_id is None:
        matched_monsters = fuzzy_search.fuzzy_search_monsters(monster_name, 5, include='large, small, elder')
        all_fuzzes = fuzzy_search.get_all_fuzz_values(matched_monsters)
        if max(all_fuzzes) < search_threshold:
            return None
    closest_monster = fuzzy_search.find_closest_match(matched_monsters)
    for monster_dict in monster_list:
        if monster_id is None:
            if len(matched_monsters) == 0:
                return None
            if monster_dict['name'] == closest_monster or monster_dict['name'].lower() == monster_name.lower():
                return monster_dict
        else:
            if monster_dict['id'] == monster_id:
                return monster_dict
    return None


def search_monsters(monster_name, search_threshold) -> MonsterList:
    matched_monsters = fuzzy_search.fuzzy_search_monsters(monster_name, 5, include='large, small, elder')
    all_fuzzes = fuzzy_search.get_all_fuzzes(matched_monsters, threshold=search_threshold)
    return all_fuzzes


def define_all_monsters(cursor, img_path) -> MonsterList:
    # Retrieves all raw monster_images data from the monster_images table, and puts it into a list.
    # Format: [(id, etc...), (id, etc...), ...]
    monster_query = '''SELECT * FROM monster'''
    all_monsters = [x for x in cursor.execute(monster_query)]

    # Stores  extracted monster_images data.
    monster_list = []

    # Retrieves all table column names to properly assign values into keys in the monster_images dictionary.
    monster_columns_query = '''SELECT name FROM PRAGMA_TABLE_INFO('monster');'''
    monster_dict_cols = []
    for col in cursor.execute(monster_columns_query):
        monster_dict_cols.append(col[0])

    # Extracts the data from the raw monster_images data list and creates a list of monster_images dictionaries.
    for monster_data in all_monsters:
        monster_dict = {}
        for i, data_point in enumerate(monster_data):
            monster_dict[monster_dict_cols[i]] = data_point

        # Add the monster_images name to the dictionary from the monster_text table.
        monster_name_query = f'''SELECT name FROM monster_text WHERE id = "{monster_data[0]}" AND lang_id = "en"'''
        monster_dict['name'] = cursor.execute(monster_name_query).fetchone()[0]

        # Add the monster_images location to the dictionary from the monster_habitat and location_text tables.
        monster_dict['locations'] = []
        monster_loc_id_query = f'''SELECT location_id FROM monster_habitat WHERE monster_id = "{monster_data[0]}"'''
        monster_loc_ids = [x[0] for x in cursor.execute(monster_loc_id_query)]
        if monster_loc_ids is not None:
            # Iterate through location_ids and search the location_text table to retrieve the location name.
            for loc_id in monster_loc_ids:
                location_query = f'''SELECT name FROM location_text WHERE id = "{loc_id}" AND lang_id = "en"'''
                all_locations = cursor.execute(location_query)
                for location_name in all_locations:
                    monster_dict['locations'].append(location_name[0])

        # Add the monster_images image file name from the stored offline images.
        monster_dict['image'] = None
        for img_file in listdir(img_path):
            file_name = img_file.split('.')[0]
            if int(file_name) == int(monster_dict['id']):
                monster_dict['image'] = f'{file_name}'

        # Append the generated monster dictionary to the list of monster dictionaries.
        monster_list.append(monster_dict)
    return monster_list
