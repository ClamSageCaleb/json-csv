import os
from pathlib import Path
import pandas as pd
from flatten_json import flatten
from collections import OrderedDict
import json
import re

variableDir = r'../variables/'
jsonDir = r'../jsons/'

if not os.path.exists(variableDir):
    print("\nCouldn't find directories: \n" + 
    "\t- variables\n")
    # Creates directories
    os.makedirs(variableDir)
else:
    print("\nVariables found\n")

variables = ["ID"]
test = {}

for i in range(1, 301):
    weightMax = f"Day{i}WeightMax"
    weightMin = f"Day{i}WeightMin"
    steps = f"Day{i}Steps"
    sysMin = f"Day{i}SystolicMin"
    sysMax = f"Day{i}SystolicMax"
    diaMin = f"Day{i}DiastolicMin"
    diaMax = f"Day{i}DiastolicMax"
    kcal = f"Day{i}KcalEnergyConsumed"
    ds = f"Day{i}DietarySodium"
    variables.extend((weightMax, weightMin, steps, sysMin, sysMax, diaMin, diaMax, kcal, ds))


dataFrame = pd.DataFrame(columns=list(variables))
dataFrame.to_csv(variableDir + "variablesCSV.csv", index=False)



