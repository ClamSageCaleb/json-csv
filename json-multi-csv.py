import os
import pandas as pd
from pathlib import Path
from flatten_json import flatten
import re
import json

jsonDir = r'./jsons/'
jsonDone = r'./jsons-done/'
csvVertPath = r'./data-converted-vertical/'
csvHorizPath = r'./data-converted-horizontal/'


if not os.path.exists(csvVertPath and csvHorizPath and jsonDir and jsonDone):
    print("\nCouldn't find directories: \n" + 
    "\t- jsons\n" + 
    "\t- data-conversion-vertical\n" +  
    "\t- data-conversion-horizontal\n" +
    "\t- jsons-done\n" +
    "\nCreating directories now.")
    os.makedirs(csvVertPath)
    os.makedirs(csvHorizPath)
    os.makedirs(jsonDir)
    os.makedirs(jsonDone)
else:
    print("\nDirectories found: \n" + 
    "\t- jsons\n" + 
    "\t- data-conversion-vertical\n" +  
    "\t- data-conversion-horizontal\n" +
    "\t- jsons-done\n")

sDict = {}
fitbit = 'related_PatientHealthResult_'

print("\nPlease place all JSON files in the jsons directory. \n")
directory = input("Press any key to continue... ")
print("\nBeginning conversion...\n")

for filename in os.listdir(jsonDir):
    if filename.endswith(".json"): 
        p = Path(jsonDir + "\\" + filename)
        root, ext = os.path.splitext(filename)
        # read json
        with p.open('r', encoding='utf-8') as f:
            d = json.load(f)
        flat_json = (flatten(d))

        # Selecting important elements from the flat_json dictionary
        sDict['display_name'] = flat_json['display_name']
        sDict['_primary_coach'] = flat_json['_primary_coach']
        sDict['birth_date'] = flat_json['birth_date']
        for key in flat_json:
            if key == 'gender':
                sDict['gender'] = flat_json['gender']
            else:
                continue
        sDict['email_address'] = flat_json['email_address']

        # Filtering the original dictionary by data and placing it in a new dictionary called sDict
        for key in flat_json:
            for m in re.finditer(fitbit, key):
                for n in re.finditer('_data_value', key):
                    sDict[key.replace(fitbit, "Value ").replace("_data_value", "")] = flat_json[key]

                for n in re.finditer('_data_systolic_value', key):
                    sDict[key.replace(fitbit, "Systolic Value ").replace("_data_systolic_value", "")] = flat_json[key]

                for n in re.finditer('_data_systolic_unit', key):
                    sDict[key.replace(fitbit, "Systolic Unit ").replace("_data_systolic_unit", "")] = flat_json[key]

                for n in re.finditer('_data_diastolic_value', key):
                    sDict[key.replace(fitbit, "Diastolic Value ").replace("_data_diastolic_value", "")] = flat_json[key]
                    
                for n in re.finditer('_data_diastolic_unit', key):
                    sDict[key.replace(fitbit, "Diastolic Unit ").replace("_data_diastolic_unit", "")] = flat_json[key]

                for n in re.finditer('_data_unit', key):
                    sDict[key.replace(fitbit, "Unit ").replace("_data_unit", "")] = flat_json[key]
               
                for n in re.finditer('_occurred_at_local_time', key):
                    sDict[key.replace(fitbit, "Occurred_At ").replace("_occurred_at", "")] = flat_json[key]
            
                for n in re.finditer('_updated_at', key):
                    sDict[key.replace(fitbit, "Updated_At ").replace("_updated_at", "")] = flat_json[key]

                for n in re.finditer('_metric_type', key):
                    sDict[key.replace(fitbit, "Metric ").replace("_metric_type", "")] = flat_json[key]
        
        # create dataframe
        #df = pd.DataFrame.from_dict(flat_json, orient="index")
        dfFiltered = pd.DataFrame.from_dict(sDict, orient="index")

        # create excel (vertical) readable file
        dfFiltered.to_csv(csvVertPath + root + '.csv', index=True, encoding="utf-8")

        # create excel (horizontal) readable file
        dfFiltered = pd.json_normalize(sDict)
        dfFiltered.to_csv(csvHorizPath + root + '(format).csv', index=True, encoding="utf-8")

        print("\n" + root + ".csv is complete. " + root + "(format.csv) is complete." +
        "\nCheck the data-converted directories for your files.\n" + 
        "Moving " + filename + "-> jsons-done.")

        os.rename(p, jsonDone + filename)
        continue
    else:
        continue