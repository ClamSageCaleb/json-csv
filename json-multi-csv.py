import os
import pandas as pd
from pathlib import Path
from flatten_json import flatten
import json



directory = input("Path to json dir: ")

for filename in os.listdir(directory):
    if filename.endswith(".json"): 
        p = Path(directory + "\\" + filename)
        root, ext = os.path.splitext(filename)
        # read json
        with p.open('r', encoding='utf-8') as f:
            d = json.load(f)

        # create dataframe
        flat_json = (flatten(d))
        df = pd.DataFrame.from_dict(flat_json, orient="index")

        # create excel (vertical) readable file
        df.to_csv(root + '.csv', index=True, encoding="utf-8")

        # create excel (horizontal) readable file
        df = pd.json_normalize(flat_json)
        df.to_csv(root +'(format).csv', index=True, encoding="utf-8")

        print(root + ".csv is complete. " + root + "(format.csv) is complete.")
        continue
    else:
        continue