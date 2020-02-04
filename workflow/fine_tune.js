const fs = require('fs')
var stage = fs.readdirSync("../output/stage").filter(x=>x.endsWith(".svg"))
var glyphs = {}
for (var i = 0; i < stage.length; i++){
	glyphs[stage[i]]=fs.readFileSync("../output/stage/"+stage[i]).toString()
}
var xforms_str = "{}";
try{
	xforms_str = fs.readFileSync("../data/svg_tweak.json").toString()
}catch(e){

}
function make_page(){
	var W = 64;
	var NPR= 10;
	var glyph_keys = Object.keys(glyphs);
	var s = "";

	// glyph_keys = glyph_keys.filter(x=>{
	// 	if (! (x in xforms)){
	// 		return true;
	// 	}
	// 	if (xforms[x].x == 0 && xforms[x].y == 0 && xforms[x].rotate == 0 && xforms[x].scale == 1){
	// 		return true;
	// 	}
	// 	return false;
	// })
	for (var i = 0; i < glyph_keys.length; i++){
		var k = glyph_keys[i]
		s+=glyphs[k].replace(/<svg/,`<svg id="${k}"`).replace(/width="100"/,`width="${W}"`).replace(/height="100"/,`height="${W}"`);
		if (!xforms[k]){
			xforms[k] = {x:0,y:0,rotate:0,scale:1}
		}
	}
	var maindiv = document.getElementById("main");
	maindiv.innerHTML=s;

	var glyph_hl;
	for (var i = 0; i < glyph_keys.length; i++){
		glyph_hl = glyph_keys[i]
		update_xform(()=>0);
		if (i % 100 == 0){
			console.log(i,"/",glyph_keys.length);	
		}
	}
	
	var rh = W*Math.ceil(glyph_keys.length/NPR)*0.8;
	var rule = `<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="${W*1.2*NPR}" height="${rh}" style="position:absolute;left:0px;top:0px;">`

	for (var i = 0; i < glyph_keys.length; i++){
		var k = glyph_keys[i]
		var d = document.getElementById(k)
		d.style.outerHTML = glyphs[k];
		d.style.position="absolute";
		d.style.left=((i % NPR)*W*1.2)+"px"
		d.style.top=(Math.floor(i / NPR)*W*0.8)+"px"
		d.style.zIndex="100"
		d.onclick = function(){update_hl(this.id)}

		rule += `<rect x="${(i % NPR)*W*1.2+W*0.25}" y="${Math.floor(i / NPR)*W*0.8+W*0.25}" width="${W*0.5}" height="${W*0.5}" fill="none" stroke="rgba(0,0,0,0.4)"></rect>`
		rule += `<rect x="${(i % NPR)*W*1.2+W*0.15}" y="${Math.floor(i / NPR)*W*0.8+W*0.15}" width="${W*0.7}" height="${W*0.7}" fill="none" stroke="rgba(0,0,0,0.4)"></rect>`

		rule += `<line x1="${(i % NPR)*W*1.2+W*0.9}" y1="${Math.floor(i / NPR)*W*0.8+W*0.1}" x2="${(i % NPR)*W*1.2+W*0.1}" y2="${Math.floor(i / NPR)*W*0.8+W*0.9}" fill="none" stroke="rgba(0,0,0,0.2)"></line>`
		rule += `<line x1="${(i % NPR)*W*1.2+W*0.1}" y1="${Math.floor(i / NPR)*W*0.8+W*0.1}" x2="${(i % NPR)*W*1.2+W*0.9}" y2="${Math.floor(i / NPR)*W*0.8+W*0.9}" fill="none" stroke="rgba(0,0,0,0.2)"></line>`
	}
	for (var i = 0; i < NPR; i++){
		rule += `<line x1="${i*W*1.2+W*0.5}" y1="${0}" x2="${i*W*1.2+W*0.5}" y2="${rh}" fill="none" stroke="rgba(255,0,0,0.7)"></line>`
		rule += `<line x1="${i*W*1.2+W*0.2}" y1="${0}" x2="${i*W*1.2+W*0.2}" y2="${rh}" fill="none" stroke="rgba(255,0,0,0.5)"></line>`
		rule += `<line x1="${i*W*1.2+W*0.8}" y1="${0}" x2="${i*W*1.2+W*0.8}" y2="${rh}" fill="none" stroke="rgba(255,0,0,0.5)"></line>`
	}

	rule += "</svg>"
	document.getElementById("rule").innerHTML+=rule

	var hl = document.createElement("div");
	hl.style.border = "1px solid cyan";
	hl.style.position = "absolute"
	document.body.appendChild(hl)
	function update_hl(eid){
		glyph_hl = eid;
		hl.style.left = document.getElementById(eid).style.left;
		hl.style.top = document.getElementById(eid).style.top;
		hl.style.width = W+"px";
		hl.style.height = W+"px";
	}
	function update_xform(f){
		var svgin = glyphs[glyph_hl].replace(/[^ç]*<svg[^ç]*?>/g,"").replace(/<\/svg>/g,"");
		var t = xforms[glyph_hl];
		f(t);
		var gstr = `<g transform="translate(256,256) translate(${t.x},${t.y}) scale(${t.scale}) rotate(${t.rotate}) translate(-256,-256)">`
		// console.log(gstr)
		document.getElementById(glyph_hl).innerHTML = gstr+svgin+"</g>";
	}
	var rule_hidden = false;
	document.body.onkeypress = function(e){
		if (e.code=="KeyA"){
			update_xform((t)=>{t.x-=1})
		}else if (e.code=="KeyD"){
			update_xform((t)=>{t.x+=1})
		}else if (e.code=="KeyW"){
			update_xform((t)=>{t.y-=1})
		}else if (e.code=="KeyS"){
			update_xform((t)=>{t.y+=1})
		}else if (e.code=="KeyZ"){
			update_xform((t)=>{t.scale-=0.01})
		}else if (e.code=="KeyX"){
			update_xform((t)=>{t.scale+=0.01})
		}else if (e.code=="KeyQ"){
			update_xform((t)=>{t.rotate-=1})
		}else if (e.code=="KeyE"){
			update_xform((t)=>{t.rotate+=1})
		}else if (e.code=="KeyR"){
			update_xform((t)=>{t.rotate=0;t.x=0;t.y=0;t.scale=1})
		}else if (e.code=="KeyF"){
			saveData(JSON.stringify(xforms),"svg-tweak-"+(new Date()).getTime().toString()+".json")
		}else if (e.code=="KeyH"){
			rule_hidden = !rule_hidden
			document.getElementById("rule").style.opacity=rule_hidden?"0":"1"
		}
	}

}

var html = `
<!-- GENERATED FILE DONT EDIT --->
<body>
<div id="main">
</div>
<div id="rule">
</div>
<script>

var saveData = (function () {
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    return function (data, fileName) {
        var json = data,
            blob = new Blob([json], {type: "octet/stream"}),
            url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(url);
    };
}());


var glyphs = ${JSON.stringify(glyphs)}
var make_page = ${make_page.toString()}
var xforms = ${xforms_str};
make_page();
</script>
</body>
`
fs.writeFileSync("../tmp/fine_tweak.html",html)
