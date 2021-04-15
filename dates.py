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
datesPath = r'./dates/'


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
            for n in re.finditer('_created_at', key):
                # Renaming key from occured_at_local_time to Occured_At to be more easily called later.
                orig[key.replace(fitbit, "Occurred_At ").replace("_created_at", "")] = ref[key]
            
    return orig


def main(): 
    if not os.path.exists(datesPath):
        print("\nCouldn't find dates directory: \n" + 
        "\nCreating directory now.")
        # Creates directories
        os.makedirs(datesPath)
    else:
        print("\nDirectory found")
    start = time.time()
    print("\nBeginning date extraction...\nTime: " + time.ctime() + "\n")
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

            # create excel file
            df.to_excel(datesPath + flat_json["display_name"] + '_dates.xlsx', index=False, encoding="utf-8")
    
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