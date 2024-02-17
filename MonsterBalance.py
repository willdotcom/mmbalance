import xml.etree.ElementTree as ET
import ctypes

ico_path = 'C:\PythonMU/mu.ico'
ctypes.windll.kernel32.SetConsoleIcon(ico_path)


def modify_xml(xml_file, config_file, spawn_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    config_tree = ET.parse(config_file)
    config_root = config_tree.getroot()

    mod_enable = bool(int(config_root.get('Enable')))
    percent_increase = bool(int(config_root.get('PercentIncrease')))
    percent_decrease = bool(int(config_root.get('PercentDecrease')))
    monster_percent_change = int(config_root.get('MonsterPercentChange'))

    active_options = [option for option in ['MonsterLevelSetting', 'MonsterIndexSetting', 'MonsterMapSetting']
                      if int(config_root.find(option).get('Enable'))]

    if len(active_options) != 1:
        raise ValueError("Exactly one modification option (MonsterLevelSetting, MonsterIndexSetting, or MonsterMapSetting) "
                         "should be enabled.")

    attributes_to_modify = [
        "HP",
        "MP",
        "DamageMin",
        "DamageMax",
        "ExtraDamageMin",
        "ExtraDamageMax",
        "Defense",
        "MagicDefense",
        "ExtraDefense",
        "AttackRate",
        "BlockRate",
        "MoveRange",
        "AttackType",
        "AttackRange",
        "ViewRange",
        "MoveSpeed",
        "AttackSpeed",
        "RegenTime",
        "Attribute",
        "IceRes",
        "PoisonRes",
        "LightRes",
        "FireRes",
        "PentagramMainAttrib",
        "PentagramAttribPattern",
        "PentagramDamageMin",
        "PentagramDamageMax",
        "PentagramAttackRate",
        "PentagramDefenseRate",
        "PentagramDefense",
        "EliteMonster",
        "PunishImmune",
        "DamageAbsorption",
        "CriticalDamageRes",
        "ExcellentDamageRes",
        "DebuffApplyRes",
        "DamageCorrection",
        "ExpLevel"
    ]

    total_updated_lines = 0

    # Exclude Mobs Settings
    mobs_to_exclude_npc = set(int(index) for index in config_root.find('ExcludeMobsSetting').find('MobsToExclude').get('NPCList', '').split(',') if index)
    mobs_to_exclude_mobs = set(int(index) for index in config_root.find('ExcludeMobsSetting').find('MobsToExclude').get('MobsList', '').split(',') if index)

    for monster in root.findall(".//Monster"):
        level = int(monster.get("Level", 0))
        index = int(monster.get("Index", 0))

        # Check if the monster should be excluded based on NPC list or Mobs list
        if index in mobs_to_exclude_npc or index in mobs_to_exclude_mobs:
            continue  # Skip this monster if it should be excluded

        # Remaining logic for modification...
        if 'MonsterLevelSetting' in active_options:
            enable_mod = bool(int(config_root.find('MonsterLevelSetting').get('Enable')))
            min_val = int(config_root.find('MonsterLevelSetting').get('MonsterMinLevel'))
            max_val = int(config_root.find('MonsterLevelSetting').get('MonsterMaxLevel'))
            if enable_mod and min_val <= level <= max_val:
                apply_modification = True
            else:
                apply_modification = False

        elif 'MonsterIndexSetting' in active_options:
            enable_mod = bool(int(config_root.find('MonsterIndexSetting').get('Enable')))
            min_val = int(config_root.find('MonsterIndexSetting').get('MonsterMinIndex'))
            max_val = int(config_root.find('MonsterIndexSetting').get('MonsterMaxIndex'))
            if enable_mod and min_val <= index <= max_val:
                apply_modification = True
            else:
                apply_modification = False

        elif 'MonsterMapSetting' in active_options:
            enable_mod = bool(int(config_root.find('MonsterMapSetting').get('Enable')))
            maps_to_change = [int(m) for m in config_root.find('MonsterMapSetting/MapToChange').get('List').split(",")]
            if enable_mod and index in get_monster_indices(spawn_file, maps_to_change):
                apply_modification = True
            else:
                apply_modification = False

        if apply_modification:
            for attribute in attributes_to_modify:
                original_value = monster.get(attribute)

                # Modify values based on chosen option
                percentage_change = monster_percent_change
                if percent_increase and int(config_root.find('MonsterListMod').find('Monster').get(attribute)):
                    monster.set(attribute, str(int(float(original_value) * (1 + percentage_change / 100))))
                elif percent_decrease and int(config_root.find('MonsterListMod').find('Monster').get(attribute)):
                    monster.set(attribute, str(int(float(original_value) * (1 - percentage_change / 100))))

            # Output message indicating the modifications
            print(f"Modified Monster (Index {monster.get('Index')}):")
            for attribute in attributes_to_modify:
                print(f"  Original {attribute}: {monster.get(attribute)}, Modified {attribute}: {monster.get(attribute)}")
            print("-" * 30)

            total_updated_lines += 1

    tree.write("MonsterList_modified.xml")
    print(f"Total lines updated: {total_updated_lines}")


def get_monster_indices(spawn_file, maps_to_change):
    indices = set()
    spawn_tree = ET.parse(spawn_file)
    spawn_root = spawn_tree.getroot()
    for map_element in spawn_root.findall(".//Map"):
        map_number = int(map_element.get("Number"))
        if map_number in maps_to_change:
            for spawn_element in map_element.findall(".//Spawn"):
                monster_index = int(spawn_element.get("Index"))
                indices.add(monster_index)
    return indices


# Read the configuration from 'config.xml'
modify_xml('MonsterList.xml', 'config.xml', 'MonsterSpawn.xml')
