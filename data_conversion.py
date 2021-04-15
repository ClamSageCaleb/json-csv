import os
import pandas as pd
import numpy as np
from pathlib import Path
from flatten_json import flatten
import re
import json
import time



# Directories for the jsons and the converted xslx files
jsonDir = r'./jsons/'
jsonDone = r'./jsons-done/'
csvPath = r'./data-converted/'

# TODO: date not important, switch to day 1 - day n 
# add back empty columns
# add id numbers 
# each row a id, each column a variable (d1step d1weight etc)

def get_column_array(df, column):
    '''
    Drops empty values and empty cells.

    :param DataFrame df: The dataframe to be modified
    :param arr column: Column to be examined if empty 
    :return: Returns the modified column array without empty values
    '''
    expected_length = len(df)
    # Drops empty values
    current_array = df[column].dropna().values
    # Removes empty cells from the Dataframe
    if len(current_array) < expected_length:
        current_array = np.append(current_array, [''] * (expected_length - len(current_array)))
    return current_array

def filtered(orig, ref):
    '''
    Renames keys and extracts important data from the original json

    :param dict orig: The dictionary to be returned with the new/renamed data
    :param dict ref: The reference dictionary that contains all of the json data
    :return: The new dictionary with renamed keys and important data
    '''

    fitbit = 'related_PatientHealthResult_'

    # Filtering the original dictionary by data and placing it in a new dictionary called sDict
    for key in ref:
        for m in re.finditer(fitbit, key):
            for n in re.finditer('_data_value', key):
                # Renaming key from data_value to Value to be more easily called later.
                orig[key.replace(fitbit, "Value ").replace("_data_value", "")] = ref[key]

            for n in re.finditer('_data_systolic_value', key):
                # Renaming key from data_systolic_value to Systolic Value to be more easily called later.
                orig[key.replace(fitbit, "Systolic Value ").replace("_data_systolic_value", "")] = ref[key]

            for n in re.finditer('_data_systolic_unit', key):
                # Renaming key from data_systolic_unit to Systolic Unit Value to be more easily called later.
                orig[key.replace(fitbit, "Systolic Unit ").replace("_data_systolic_unit", "")] = ref[key]

            for n in re.finditer('_data_diastolic_value', key):
                # Renaming key from data_diastolic_value to Diastolic Value to be more easily called later.
                 orig[key.replace(fitbit, "Diastolic Value ").replace("_data_diastolic_value", "")] = ref[key]
                    
            for n in re.finditer('_data_diastolic_unit', key):
                # Renaming key from data_diastolic_unit to Diastolic Unit to be more easily called later.
                orig[key.replace(fitbit, "Diastolic Unit ").replace("_data_diastolic_unit", "")] = ref[key]

            for n in re.finditer('_data_unit', key):
                # Renaming key from data_unit to Unit to be more easily called later.
                orig[key.replace(fitbit, "Unit ").replace("_data_unit", "")] = ref[key]
               
            for n in re.finditer('_created_at', key):
                # Renaming key from occured_at_local_time to Occured_At to be more easily called later.
                orig[key.replace(fitbit, "Occurred_At ").replace("_created_at", "")] = ref[key]
            
            for n in re.finditer('_metric_type', key):
                # Renaming key from metric_type to Metric to be more easily called later.
                orig[key.replace(fitbit, "Metric ").replace("_metric_type", "")] = ref[key]
    
    return orig

def dfformat(df, dict):
    '''
    Iterates through the dictionary and matches dates in order to append data by day

    :param DataFrame df: DataFrame that has the days listed as the column headers
    :param dict dict: Dictionary containing the values that will be compared by date
    :return: DataFrame with the appended data
    '''

    # Iterates through the days in the dataframe
    d = 0
    for day in df.columns:
        # Iteratres through the keys in the dict
        d += 1
        for key in dict:
            # Compares the date to the Occured_At key in the dictionary
            for n in re.finditer('Occurred_At ', key):
                # Comapres by date instead of date and time
                if day == dict[key].split('T')[0]:
                    # Finds the key number from the dictionary in order to get matching data
                    num = re.findall(r'\d+', key)
                    numStr = ''.join(num)
                    valNum = "Value " + numStr
                    sysNum = "Systolic Value " + numStr
                    sysUnitNum = "Systolic Unit " + numStr
                    diaNum = "Diastolic Value " + numStr
                    diaUnitNum = "Diastolic Unit " + numStr
                    unitNum = "Unit " + numStr
                    metricNum = "Metric " + numStr
                    # Checks if the value is in the dictionary
                    if valNum in dict and unitNum in dict:
                        # Gets value from the key 
                        stepWeight = dict[valNum]
                        swUnit = dict[unitNum]
                        swMetric = dict[metricNum]
                        if swMetric == "weight":
                            df = df.append({f"Day{d}Weight": int(stepWeight)}, ignore_index=True)
                        elif swMetric == "step_count":
                            df = df.append({f"Day{d}Steps": int(stepWeight)}, ignore_index=True)
                        elif swMetric == "dietary_sodium":
                            df = df.append({f"Day{d}DietarySodium": int(stepWeight)}, ignore_index=True) 
                        elif swMetric == "dietary_energy_consumed":
                            df = df.append({f"Day{d}KcalEnergyConsumed": int(stepWeight)}, ignore_index=True) 
                    # Checks if the systolic value exists
                    if sysNum in dict and sysUnitNum in dict:
                        # Gets systolic value from key
                        sysVal = dict[sysNum]
                        sysUnit = dict[sysUnitNum]
                        sysMetric = dict[metricNum]
                        # Creates data and appeneds it to the dataframe
                        df = df.append({f"Day{d}Systolic": int(sysVal)}, ignore_index=True)
                    # Checks if the diastolic value exists
                    if diaNum in dict and diaUnitNum in dict:
                        # Gets diastolic value from key
                        diaVal = dict[diaNum]
                        diaUnit = dict[diaUnitNum]
                        diaMetric = dict[metricNum]
                        # Creates data and appeneds it to the dataframe
                        df = df.append({f"Day{d}Diastolic": int(diaVal)}, ignore_index=True)   
       
    return df

def main(): 
    start = time.time()
    print("\nBeginning conversion...\nTime: " + time.ctime() + "\n")
    for filename in os.listdir(jsonDir):
        sDict = {}
        days = {}
        if filename.endswith(".json"): 
            p = Path(jsonDir + "/" + filename)
            root, ext = os.path.splitext(filename)

            # Read json files
            with p.open('r', encoding='utf-8') as f:
                d = json.load(f)
            flat_json = (flatten(d))
            flat_json = {k:v for k,v in flat_json.items() if v is not None}
            sDict = filtered(sDict, flat_json)
       
            # Takes value from Occurred_At key and places the value in a dictionary of days
            for key, v in sDict.items():
                for n in re.finditer('Occurred_At', key):
                    date = v.split('T')[0]
                    days[date] = None
        
            # Sorts the days dictionary
            sDays = days.keys()

            # Create dataframe
            df = pd.DataFrame(columns=sDays)

            df = dfformat(df, sDict)

            for column in df.columns:
                df[column] = get_column_array(df, column)
                df[column].replace('', np.nan, inplace=True)
            df = df.dropna(axis=1, how='all')

            # create excel file
            df.to_excel(csvPath + flat_json["display_name"] + '.xlsx', index=False, encoding="utf-8")
    
            print("\n" + flat_json["display_name"] + ".xlsx is complete. " +  "\nCheck the data-converted directories for your files.\n" + "Moving " + filename + " -> jsons-done.\n")

            os.rename(p, jsonDone + filename)
            continue
        else:
            continue
    done = time.time()
    elapsed = round((done - start) / 60)
    print("File transfer complete!\nTime: " + time.ctime() + "\n" + "Time taken: " + str(elapsed) + " minutes")

if __name__ == "__main__":
    main()