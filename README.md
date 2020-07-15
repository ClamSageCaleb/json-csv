<h1 align="center">
  <br>
    JSON to Excel converter for FitBit json files
  <br>
</h1>

<h4 align="center">A simple python script that does json -> xlsx conversion</h4>
<br>

## Running
<br>1. Clone the Directory<br>
<br>&emsp;Repo: ```git clone https://github.com/clamsagecaleb/json-csv.git```<br>
<br>2. Ensure you have Python3 / NodeJS / TypeScript installed<br>
<br>&emsp;Python3: https://www.python.org/downloads/<br>
<br>&emsp;NodeJS: https://nodejs.org/en/<br>
<br>&emsp;TypeScript: ```npm -g install typescript```<br>
<br>3. Open terminal/powershell and compile json.ts<br>
<br>&emsp;Compile json.ts: ```tsc json.ts```<br>
<br>&emsp;Run: ```node json.js```<br>

## Process
<br> After running the json.js file, the json.js file will eventually <br>
call on the json-spss.py file. Once this file runs the following folders will <br>
be made in the working directory:<br>
```
Working Directory: ./json-csv
                    | jsons
                    | jsons-done
                    | data-converted.

Please place all JSON files in the jsons directory.
Ten seconds before conversion begins...
```
<br> Once you have placed all of the files into the json folder, <br>
the converted data while be moved to ```data-converted``` and the json <br>
will be moved to ```jsons-done```
---
