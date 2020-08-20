import os
import pandas as pd
import numpy as np
from pathlib import Path
from flatten_json import flatten
import re
import json
from collections import OrderedDict

jsonDir = r'./jsons/'
csvPath = r'./data-converted/'
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

