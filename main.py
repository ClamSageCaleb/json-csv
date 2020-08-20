#!/usr/bin/python
import os
import pandas as pd
import numpy as np
from pathlib import Path
from flatten_json import flatten
import re
import json
from collections import OrderedDict
import data_conversion
import time

jsonDir = r'./jsons/'
jsonDone = r'./jsons-done/'
csvPath = r'./data-converted/'

# Checking if the needed directories exist
if not os.path.exists(csvPath and jsonDir and jsonDone):
    print("\nCouldn't find directories: \n" + 
    "\t- jsons\n" + 
    "\t- data-conversion\n" +
    "\t- jsons-done\n" +
    "\nCreating directories now.")
    # Creates directories
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
print("\nGathering ID's...\nTime: " + time.ctime() + "\n")

pID = {}

for filename in os.listdir(jsonDir):

    if filename.endswith(".json"): 
        p = Path(jsonDir + "/" + filename)
        root, ext = os.path.splitext(filename)

        # Read json files
        with p.open('r', encoding='utf-8') as f:
            d = json.load(f)
        flat_json = (flatten(d))
        flat_json = {k:v for k,v in flat_json.items() if v is not None}
        
        for key in flat_json:
            for m in re.finditer("^display_name$", key):
                pID[flat_json[key]] = flat_json["_id"]


sPID = OrderedDict(sorted(pID.items()))
df = pd.DataFrame.from_dict(sPID, orient='index')
df.to_csv('pID.csv', sep="\t")

print("\nID's gathered, check directory for pID.csv...\nTime: " + time.ctime() + "\n")

data_conversion.main()
