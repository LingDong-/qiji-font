var fs = require('fs');
var ttf2woff2 = require('ttf2woff2');
var input;
 
input = fs.readFileSync('../dist/qiji.ttf');
fs.writeFileSync('../dist/qiji.woff2', ttf2woff2(input));
console.log("√")

input = fs.readFileSync('../dist/qiji-fallback.ttf');
fs.writeFileSync('../dist/qiji-fallback.woff2', ttf2woff2(input));
console.log("√")


input = fs.readFileSync('../dist/qiji-combo.ttf');
fs.writeFileSync('../dist/qiji-combo.woff2', ttf2woff2(input));
console.log("√")