var fs = require('fs');
var flatten = require('flat');
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
    var rawdata = fs.readFileSync('./jsons/' + arrayOfFiles[i]);
    var data = JSON.parse(rawdata);
    //var flatdata = flatten(data);
    var fb = data.related.PatientHealthResult;
    for (var y = 0; y < fb.length; y++) {
        if(fb[y].occurred_at_local_time !== undefined && fb[y].data.value !== undefined && fb[y].data.value !== null) {
            var jsonData = `{"${arrayOfFiles[i]}":[{"Date ${y}": "${fb[y].occurred_at_local_time}", 
            "Data ${y}": "${fb[y].data.value} ${fb[y].data.unit}"}]}`;
            var jsonObj = JSON.parse(jsonData);
            var jsonContents = JSON.stringify(jsonObj, null, 4);
            console.log(jsonContents);
        };
    };
    var move = './jsons-for-py/' + arrayOfFiles[i];
    var orig = './jsons/' + arrayOfFiles[i]
    fs.rename(orig, move, function(err) {
        if (err) throw err;
    });
};
console.log('All files have been moved...\n')
console.log('Starting json-spss.py...\n')

let o = {
    mode: 'text',
    pythonOptions: ['-u'],
  };

let shell = new PythonShell('json-spss.py', o as any);
shell.on('message', function (message) {
    console.log(message);
  });
