import os
import pandas as pd
import numpy as np
from pathlib import Path
from flatten_json import flatten
import re
import json
import time

jsonDir = r'./jsons-for-py/'
jsonDone = r'./jsons-done/'
csvPath = r'./data-converted/'

def get_column_array(df, column):
    expected_length = len(df)
    current_array = df[column].dropna().values
    if len(current_array) < expected_length:
        current_array = np.append(current_array, [''] * (expected_length - len(current_array)))
    return current_array

def filtered(orig, ref):

    fitbit = 'related_PatientHealthResult_'

    # Filtering the original dictionary by data and placing it in a new dictionary called sDict
    for key in ref:
        for m in re.finditer(fitbit, key):
            for n in re.finditer('_data_value', key):
                orig[key.replace(fitbit, "Value ").replace("_data_value", "")] = ref[key]

            for n in re.finditer('_data_systolic_value', key):
                orig[key.replace(fitbit, "Systolic Value ").replace("_data_systolic_value", "")] = ref[key]

            for n in re.finditer('_data_systolic_unit', key):
                orig[key.replace(fitbit, "Systolic Unit ").replace("_data_systolic_unit", "")] = ref[key]

            for n in re.finditer('_data_diastolic_value', key):
                 orig[key.replace(fitbit, "Diastolic Value ").replace("_data_diastolic_value", "")] = ref[key]
                    
            for n in re.finditer('_data_diastolic_unit', key):
                orig[key.replace(fitbit, "Diastolic Unit ").replace("_data_diastolic_unit", "")] = ref[key]

            for n in re.finditer('_data_unit', key):
                orig[key.replace(fitbit, "Unit ").replace("_data_unit", "")] = ref[key]
               
            for n in re.finditer('_occurred_at_local_time', key):
                orig[key.replace(fitbit, "Occurred_At ").replace("_occurred_at", "")] = ref[key]
            
            for n in re.finditer('_metric_type', key):
                orig[key.replace(fitbit, "Metric ").replace("_metric_type", "")] = ref[key]
    
    return orig

def dirs():
    if not os.path.exists(csvPath and jsonDir and jsonDone):
        print("\nCouldn't find directories: \n" + 
        "\t- jsons\n" + 
        "\t- data-conversion\n" +
        "\t- jsons-done\n" +
        "\nCreating directories now.")
        os.makedirs(csvPath)
        os.makedirs(jsonDir)
        os.makedirs(jsonDone)
    else:
        print("\nDirectories found: \n" + 
        "\t- jsons\n" + 
        "\t- data-conversion\n" +
        "\t- jsons-done\n")

    print("\nPlease place all JSON files in the jsons directory.\nTen seconds before conversion begins...\n")
    time.sleep(10)
    print("\nBeginning conversion...\nTime: " + time.ctime() + "\n")

def dfformat(df, dict):
    for day in df.columns:
        for key in dict:
            for n in re.finditer('Occurred_At ', key):
                if day == dict[key].split('T')[0]:
                    num = re.findall(r'\d+', key)
                    numStr = ''.join(num)
                    # TODO bug might be here, only finds value not Systolic Value or Diastolic Value
                    val = "Value " + numStr
                    sys = "Systolic Value " + numStr
                    sunit = "Systolic Unit " + numStr
                    dia = "Diastolic Value " + numStr
                    dunit = "Diastolic Unit " + numStr
                    unit = "Unit " + numStr
                    metric = "Metric " + numStr
                    if val in dict and unit in dict:
                        x = dict[val]
                        y = dict[unit]
                        z = dict[metric]
                        data = f"{x} {y} {z}"
                        #data = str(x) + ' ' + y + ' ' + z
                        df = df.append({day: data}, ignore_index=True)
                    if sys in dict and sunit in dict:
                        s = dict[sys]
                        su = dict[sunit]
                        z = dict[metric]
                        dataTest = f"{s} {su} {z}"
                        #dataTest = str(s) + ' ' + su + ' ' + metric
                        df = df.append({day: dataTest}, ignore_index=True)
                    if dia in dict and dunit in dict:
                        d = dict[dia]
                        du = dict[dunit]
                        z = dict[metric]
                        dataTestDia = f"{d} {du} {z}"
                        #dataTestDia = str(d) + ' ' + du + ' ' + metric
                        df = df.append({day: dataTestDia}, ignore_index=True)                 
    return df

def js_output():
    output = "\n" + root + ".xlsx is complete. " +  "\nCheck the data-converted directories for your files.\n" + "Moving " + filename + " -> jsons-done.\n"
    print(output)

dirs()

for filename in os.listdir(jsonDir):
    sDict = {}
    days = {}
    if filename.endswith(".json"): 
        p = Path(jsonDir + "/" + filename)
        root, ext = os.path.splitext(filename)

        # read json
        with p.open('r', encoding='utf-8') as f:
            d = json.load(f)
        flat_json = (flatten(d))
        flat_json = {k:v for k,v in flat_json.items() if v is not None}

        sDict = filtered(sDict, flat_json)
       
        for key, v in sDict.items():
            for n in re.finditer('Occurred_At', key):
                date = v.split('T')[0]
                days[date] = None
        
        sDays = sorted(days.keys())

        # create dataframe
        df = pd.DataFrame(columns=list(sDays))

        df = dfformat(df, sDict)

        for column in df.columns:
            df[column] = get_column_array(df, column)

        df = pd.DataFrame.drop_duplicates(df)

        # create excel file
        df.to_excel(csvPath + root + '.xlsx', index=False, encoding="utf-8")
    
        js_output()

        os.rename(p, jsonDone + filename)
        continue
    else:
        continue

print("File transfer complete!\nTime: " + time.ctime() + "\n")