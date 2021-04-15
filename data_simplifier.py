import os
import pandas as pd
import numpy as np
from pathlib import Path
from flatten_json import flatten
import re
import json
import time
import data_conversion



# Directories for the jsons and the converted xslx files
jsonDir = r'./jsons/'
jsonDone = r'./jsons-done/'
csvPath = r'./data-converted/'
finalPath = r'./final-data/'

def main():
    start = time.time()
    print("\nBeginning Simplifcation process...\nTime: " + time.ctime() + "\n")
    cols = []
    for x in range(1, 301):
        cols.append(f"Day{x}WeightMax")
        cols.append(f"Day{x}WeightMin")
        cols.append(f"Day{x}Steps")
        cols.append(f"Day{x}SystolicMin")
        cols.append(f"Day{x}SystolicMax")
        cols.append(f"Day{x}DiastolicMin")
        cols.append(f"Day{x}DiastolicMax")
        cols.append(f"Day{x}KcalEnergyConsumed")
        cols.append(f"Day{x}DietarySodium")
        
    for filename in os.listdir(csvPath):
        if filename.endswith(".xlsx"): 
            p = Path(csvPath + "/" + filename)
            root, ext = os.path.splitext(filename)

            df = pd.read_excel(p)
            mmDF = pd.DataFrame(columns=cols)

            for x in df.columns:
                max = df[x].max()
                min = df[x].min()
                if("Steps" in x or "DietarySodium" in x or "KcalEnergyConsumed" in x):
                    mmDF = mmDF.append({x: max}, ignore_index=True)
                else:
                    mmDF = mmDF.append({x + "Max": max}, ignore_index=True)
                    mmDF = mmDF.append({x + "Min": min}, ignore_index=True)

            for col in mmDF.columns:
                mmDF[col] = data_conversion.get_column_array(mmDF, col)
                mmDF[col].replace('', np.nan, inplace=True)

            mmDF.to_excel(finalPath + filename)
            print("\n" + filename + " is complete. " +  "\nCheck the final-data directories for your files.\n")
            continue
        else:
            continue
    done = time.time()
    elapsed = round((done - start) / 60)
    print("File simplification complete!\nTime: " + time.ctime() + "\n" + "Time taken: " + str(elapsed) + " minutes")

if __name__ == "__main__":
    main()