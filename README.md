<h1 align="center">
  <br>
    JSON to Excel converter for FitBit json files 📂
  <br>
  <br>
    JSON -> Excel -> Formatted Excel -> SPSS
  <br>
</h1>

<h4 align="center">A simple python script that does json -> xlsx conversion for SPSS usage.</h4>
<br>

## Running 👟
<br>1. Clone the Directory<br>
<br>&emsp;Repo: ```git clone https://github.com/clamsagecaleb/json-csv.git```<br>
<br>2. Ensure you have Python3 installed<br>
<br>&emsp;Python3: https://www.python.org/downloads/<br>
<br>3. Running the script<br>
<br>&emsp;Run: ```pip install -r requirements.txt```
<br>&emsp;Run: ```python main.py```<br>

## Process 📈
<br> Once this file runs the following folders will be made in the working directory:<br>

```
Working Directory: ./json-csv
                    | jsons
                    | jsons-done
                    | data-converted.
                    | final-data

Please place all JSON files in the jsons directory.
Ten seconds before conversion begins...
```
<br> Once you have placed all of the files into the json folder, <br>
the converted data while be moved to ```data-converted``` and the json <br>
will be moved to ```jsons-done```. 

<br>Once the data is in ```data-converted``` the script will <br>
open the files and format them in a more readable format. <br>
The readable files will be placed in ```final-data```.

---
