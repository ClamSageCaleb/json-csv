import pandas as pd
from pathlib import Path
from flatten_json import flatten
import json

jsonPath = input("Path to json file: ")
jsonPath = jsonPath.replace('"', '') 

# set path to file
p = Path(jsonPath)

# read json
with p.open('r', encoding='utf-8') as f:
    d = json.load(f)

# create dataframe
flat_json = (flatten(d))
df = pd.DataFrame.from_dict(flat_json, orient="index")

# create excel (test 1) readable file
df.to_csv('test.csv', index=True, encoding="utf-8")

# create excel (test 2) readable file
df = pd.json_normalize(flat_json)
df.to_csv('test2.csv', index=True, encoding="utf-8")
