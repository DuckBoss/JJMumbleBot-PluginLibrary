from JJMumbleBot.plugins.extensions.mhw_wiki.resources.monster_names import monsters_storage_large, \
    monsters_storage_elder, monsters_storage_small, monsters_storage_endemic
from fuzzywuzzy import process


def find_closest_match(fuzzy_list):
    match_dict = {}
    for i, item in enumerate(fuzzy_list):
        match_dict[item[0]] = item[1]
    return max(match_dict, key=match_dict.get)


def get_all_fuzz_values(fuzzy_list):
    values_list = []
    for i, item in enumerate(fuzzy_list):
        values_list.append(item[1])
    return values_list


def get_all_fuzzes(fuzzy_list, threshold=0):
    fuzz_list = []
    for item in fuzzy_list:
        if int(item[1]) >= threshold:
            fuzz_list.append(item)
    return fuzz_list


def fuzzy_search_monsters(name, limit, include='all'):
    matched_monsters = []
    if include == 'all':
        matched_monsters += process.extract(name, monsters_storage_elder, limit=limit)
        matched_monsters += process.extract(name, monsters_storage_large, limit=limit)
        matched_monsters += process.extract(name, monsters_storage_small, limit=limit)
        matched_monsters += process.extract(name, monsters_storage_endemic, limit=limit)
    else:
        if 'elder' in include:
            matched_monsters += process.extract(name, monsters_storage_elder, limit=limit)
        if 'large' in include:
            matched_monsters += process.extract(name, monsters_storage_large, limit=limit)
        if 'small' in include:
            matched_monsters += process.extract(name, monsters_storage_small, limit=limit)
        if 'endemic' in include:
            matched_monsters += process.extract(name, monsters_storage_endemic, limit=limit)
    return matched_monsters
