import xml.etree.ElementTree as ET
import configparser
import ctypes

ico_path = 'C:\PythonMU/mu.ico'
ctypes.windll.kernel32.SetConsoleIcon(ico_path)


def modify_xml(xml_file, config_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    config = configparser.ConfigParser()
    config.read(config_file)

    percent_increase = bool(int(config['Monster']['PercentIncrease']))
    percent_decrease = bool(int(config['Monster']['PercentDecrease']))
    monster_min_index = int(config['Monster']['MonsterMinIndex'])
    monster_max_index = int(config['Monster']['MonsterMaxIndex'])
    monster_index_mod = bool(int(config['Monster']['MonsterIndexMod']))
    monster_level_mod = bool(int(config['Monster']['MonsterLevelMod']))

    if percent_increase and percent_decrease:
        raise ValueError("Please choose either PercentIncrease or PercentDecrease, not both.")

    if not percent_increase and not percent_decrease:
        raise ValueError("Please choose either PercentIncrease or PercentDecrease.")

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
        "DamageCorrection"
    ]

    total_updated_lines = 0

    for monster in root.findall(".//Monster"):
        level = int(monster.get("Level", 0))
        index = int(monster.get("Index", 0))

        if (monster_level_mod and monster_min_level <= level <= monster_max_level) or \
           (monster_index_mod and monster_min_index <= index <= monster_max_index):
            for attribute in attributes_to_modify:
                original_value = monster.get(attribute)

                # Modify values based on chosen option
                percentage_change = int(config['Monster']['MonsterPercentChange'])
                if percent_increase and int(config['Monster'][attribute]):
                    monster.set(attribute, str(int(float(original_value) * (1 + percentage_change / 100))))
                elif percent_decrease and int(config['Monster'][attribute]):
                    monster.set(attribute, str(int(float(original_value) * (1 - percentage_change / 100))))

            # Output message indicating the modifications
            print(f"Modified Monster (Index {monster.get('Index')}):")
            for attribute in attributes_to_modify:
                print(f"  Original {attribute}: {monster.get(attribute)}, Modified {attribute}: {monster.get(attribute)}")
            print("-" * 30)

            total_updated_lines += 1

    tree.write("MonsterList_modified.xml")
    print(f"Total lines updated: {total_updated_lines}")


# Read the configuration from 'config.ini'
modify_xml('MonsterList.xml', 'config.ini')
