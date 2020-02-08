const fs = require('fs')
var charset = fs.readFileSync("../data/labels_all.txt").toString().split("\n").filter(x=>x.length)
	.map(x=>[x.split("\t")[1],x.split("\t")[0].replace(".png",".svg")])
	.sort().map(x=>[x[1],x[0]])

var glyphs = {}

for (var i = 0; i < charset.length; i++){
	glyphs[charset[i][0]]=fs.readFileSync("../output/stage/"+charset[i][0]).toString().split("</metadata>")[1].split("</svg>")[0]
}
// charset = charset.slice(0,4)
// console.log(glyphs[Object.keys(glyphs)[0]])
var uw = 64
var px = 12.8
var py = -4
var cols = 30
var rows = Math.ceil(charset.length/cols)
var color_anno = "salmon"
var color_hint = "salmon"

var svgw = cols*(uw+px*2)+px
var svgh = rows*(uw+py*2)+py
var svgp = 20
var svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${(svgw+svgp*2)*0.8}" height="${(svgh+svgp*2)*0.8}" viewBox="-${svgp} -${svgp} ${svgw+svgp*2} ${svgh+svgp*2}">`
svg += `<rect x="-100" y="-100" width="${svgw+200}" height="${svgh+200}" fill="white"></rect>`
for (var i = 0; i < charset.length; i++){
	var r = i % rows
	var c = cols-Math.floor(i/rows)-1
	// console.log(r,c)
	var hex = "    "
	var char = " "
	if(charset[i][1].length == 1){
		hex = charset[i][1].charCodeAt(0).toString(16).toUpperCase()
		char = charset[i][1]
	}
	svg += `<rect x="${(uw+px*2)*c+px+uw*0.1}" y="${(uw+py*2)*r+py+uw*0.1}" width="${uw*0.8}" height="${uw*0.8}" fill="none" stroke="${color_anno}" stroke-width="0.5"></rect>`
	svg += `<text x="${(uw+px*2)*c+px+uw*0.9+5}" y="${(uw+py*2)*r+py+uw*0.1+11}" style="font-family:Courier Prime; font-size:14px" fill="${color_anno}">${hex.slice(0,2)}</text>`
	svg += `<text x="${(uw+px*2)*c+px+uw*0.9+5}" y="${(uw+py*2)*r+py+uw*0.1+22}" style="font-family:Courier Prime; font-size:14px" fill="${color_anno}">${hex.slice(2)}</text>`
	svg += `<text x="${(uw+px*2)*c+px+uw*0.9+5.5}" y="${(uw+py*2)*r+py+uw*0.9-4}" font-family="Heiti TC" style="font-size: 16px;" fill="${color_anno}">${char}</text>`

	svg += `<line x1="${(uw+px*2)*c+px+uw*0.1}" y1="${(uw+py*2)*r+py+uw*0.1}" x2="${(uw+px*2)*c+px+uw*0.9}" y2="${(uw+py*2)*r+py+uw*0.9}" fill="none" stroke="${color_hint}" stroke-dasharray="1" stroke-width="0.3"></line>`
	svg += `<line x1="${(uw+px*2)*c+px+uw*0.9}" y1="${(uw+py*2)*r+py+uw*0.1}" x2="${(uw+px*2)*c+px+uw*0.1}" y2="${(uw+py*2)*r+py+uw*0.9}" fill="none" stroke="${color_hint}" stroke-dasharray="1" stroke-width="0.3"></line>`
	
	svg += `<line x1="${(uw+px*2)*c+px+uw*0.5}" y1="${(uw+py*2)*r+py+uw*0.1}" x2="${(uw+px*2)*c+px+uw*0.5}" y2="${(uw+py*2)*r+py+uw*0.9}" fill="none" stroke="${color_hint}" stroke-dasharray="1" stroke-width="0.3"></line>`
	svg += `<line x1="${(uw+px*2)*c+px+uw*0.9}" y1="${(uw+py*2)*r+py+uw*0.5}" x2="${(uw+px*2)*c+px+uw*0.1}" y2="${(uw+py*2)*r+py+uw*0.5}" fill="none" stroke="${color_hint}" stroke-dasharray="1" stroke-width="0.3"></line>`

	svg += `<g transform="translate(${(uw+px*2)*c+px+uw/2},${(uw+py*2)*r+py+uw/2}) scale(${uw/512}) translate(-256,-256)">${glyphs[charset[i][0]]}</g>`
}
svg += "</svg>"
fs.writeFileSync("../tmp/sheet.svg",svg)