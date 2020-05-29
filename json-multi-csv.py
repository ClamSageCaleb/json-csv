import os
import pandas as pd
from pathlib import Path
from flatten_json import flatten
import re
import json

sDict = {}

directory = input("Path to json dir: ")
csvVertPath = r'./data-converted-vertical/'
csvHorizPath = r'./data-converted-horizontal/'

for filename in os.listdir(directory):
    if filename.endswith(".json"): 
        p = Path(directory + "\\" + filename)
        root, ext = os.path.splitext(filename)
        # read json
        with p.open('r', encoding='utf-8') as f:
            d = json.load(f)
        
        flat_json = (flatten(d))

        # Selecting important elements from the flat_json dictionary
        sDict['display_name'] = flat_json['display_name']
        sDict['_primary_coach'] = flat_json['_primary_coach']
        sDict['birth_date'] = flat_json['birth_date']
        sDict['gender'] = flat_json['gender']
        sDict['email_address'] = flat_json['email_address']

        # Filtering the original dictionary by data and placing it in a new dictionary called sDict
        for key in flat_json:
            for m in re.finditer('related_PatientHealthResult_', key):
                sDict[key] = flat_json[key]
        
        # create dataframe
        df = pd.DataFrame.from_dict(flat_json, orient="index")
        dfFiltered = pd.DataFrame.from_dict(sDict, orient="index")

        # create excel (vertical) readable file
        df.to_csv(csvVertPath + root + '.csv', index=True, encoding="utf-8")
        dfFiltered.to_csv(csvVertPath + root + '(TEST).csv', index=True, encoding="utf-8")

        # create excel (horizontal) readable file
        df = pd.json_normalize(flat_json)
        dfFiltered = pd.json_normalize(sDict)
        df.to_csv(csvHorizPath + root +'(format).csv', index=True, encoding="utf-8")
        dfFiltered.to_csv(csvHorizPath + root + '(TEST)(format).csv', index=True, encoding="utf-8")

        print("\n" + root + ".csv is complete. " + root + "(format.csv) is complete." +
        "\nCheck the data-converted directories for your files.\n")
        continue
    else:
        continue