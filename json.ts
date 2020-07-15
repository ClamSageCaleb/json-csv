var fs = require('fs');
var path = require('path');
import {PythonShell} from 'python-shell';
var dir = './jsons-for-py';

console.log('\nChecking for jsons-for-py...\n')
if(!fs.existsSync(dir)) {
    console.log('Making jsons-for-py...\n')
    fs.mkdirSync(dir);
} else {
    console.log('Directory Found!\n')
};


const arrayOfFiles = fs.readdirSync("./jsons")

for (var i = 0; i < arrayOfFiles.length; i++) {
    let rawdata = fs.readFileSync('./jsons/' + arrayOfFiles[i]);
    let data = JSON.parse(rawdata);
    //let fb = data.related.PatientHealthResult;
    //for (var y = 0; y < fb.length; y++) {
        //console.log("This is W.I.P.\n");
    //}
    let move = './jsons-for-py/' + arrayOfFiles[i];
    let orig = './jsons/' + arrayOfFiles[i]
    fs.rename(orig, move, function(err) {
        if (err) throw err;
    });
}

console.log('All files have been moved...\n')
console.log('Start json-spss.py...\n')

let o = {
    mode: 'text',
    pythonOptions: ['-u'],
  };

let shell = new PythonShell('json-spss.py', o as any);
shell.on('message', function (message) {
    console.log(message);
  });
