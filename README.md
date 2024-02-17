# MU Monster Balance

This Python script utilizes the `xml.etree.ElementTree` library to modify an XML file based on IGCN configuration file. The goal is to adjust specific attributes of the `Monster` tags in the XML file.

## Support Version
- Season 18
- Season 19

## To Build .exe
- Use pyinstaller
 
## Requirements to use on Env

- Python 3.x
- Python Standard Library: `xml.etree.ElementTree`

## Usage

1. Configure the modification in the `config.xml` file:
   - `MonsterPercentChange`: Percentage of change for monster attributes.
   - Other boolean values indicating which attributes to modify (1 to modify, 0 to not modify).
   - You can also enable modification based on Monster Level, Monster Index, or Map Number.
   - For modification based on Map ID, specify the map numbers in the MapToChange attribute separated by commas.

2. Run the script or .exe providing on Release section and a new `MonsterList_Modified.xml` will be generated with the changes.
3. Enjoy!

   ```bash
   python MonsterBalance.py
