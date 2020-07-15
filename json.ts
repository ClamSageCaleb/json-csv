var fs = require('fs');
var path = require('path');
import {PythonShell} from 'python-shell';


const arrayOfFiles = fs.readdirSync("./back-up")

for (var i = 0; i < arrayOfFiles.length; i++) {
    let rawdata = fs.readFileSync('./back-up/' + arrayOfFiles[i]);
    let data = JSON.parse(rawdata);
    let fb = data.related.PatientHealthResult;
    for (var y = 0; y < fb.length; y++) {
        console.log("This is W.I.P.\n");
    }
}

console.log('Start json-spss.py...\n')

let o = {
    mode: 'text',
    pythonOptions: ['-u'],
  };

let shell = new PythonShell('json-spss.py', o as any);
shell.on('message', function (message) {
    console.log(message);
  });
