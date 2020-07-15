var fs = require('fs');
var path = require('path');
import {PythonShell} from 'python-shell';


const arrayOfFiles = fs.readdirSync("./back-up")

for (var i = 0; i < arrayOfFiles.length; i++) {
    let rawdata = fs.readFileSync('./back-up/' + arrayOfFiles[i]);
    let data = JSON.parse(rawdata);
    for (var y = 0; y < data.related.PatientHealthResult.length; y++) {
        console.log(data.related.PatientHealthResult[y].occurred_at_local_time)
        console.log(data.related.PatientHealthResult[y].data.value + 
        ' ' +data.related.PatientHealthResult[y].data.unit)
        try {
            console.log(data.related.PatientHealthResult[y].data.systolic.value + 
                ' ' +data.related.PatientHealthResult[y].data.systolic.unit)
            console.log(data.related.PatientHealthResult[y].data.diastolic.value + 
                ' ' +data.related.PatientHealthResult[y].data.diastolic.unit)
        } catch (e) {
            continue
        }
        console.log('\n')
    }
}

console.log('Start json-spss.py...\n')
let o = {
    mode: 'text',
    pythonOptions: ['-u'],
  };


let shell = new PythonShell('json-spss.py', o);
shell.on('message', function (message) {
    console.log(message);
  });
