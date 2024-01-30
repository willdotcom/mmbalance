# MU Monster Balance

This Python script utilizes the `xml.etree.ElementTree` library to modify an XML file based on IGCN configuration file. The goal is to adjust specific attributes of the `Monster` tags in the XML file.


## To Build .exe
- Use pyinstaller
 
## Requirements to use on Env

- Python 3.x
- Python Standard Library: `xml.etree.ElementTree`

## Usage

1. Configure the modification in the `config.ini` file:
   - `MonsterPercentChange`: Percentage of change for monster attributes.
   - Other boolean values indicating which attributes to modify (1 to modify, 0 to not modify).
2. Run the script providing the XML file name (e.g., `MonsterList.xml`):

   ```bash
   python MonsterBalance.py MonsterList.xml
