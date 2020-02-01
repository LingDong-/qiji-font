const fs = require('fs')

var rectfiles = fs.readdirSync("../data/rects").filter(x=>x.endsWith(".tsv")).map(x=>"../data/rects/"+x)
var rects = []
var imgfiles = []
var txt = fs.readFileSync("../data/hnz_matched.txt").toString().replace(/[^\u3e00-\u9fff]/g,"");


for (var i = 0; i < rectfiles.length; i++){
	var id = rectfiles[i].split("/").slice(-1)[0].split(".")[0]
	if (!id.startsWith("H")){
		continue
	}
	var nid = parseInt(id.slice(1))
	var r = fs.readFileSync(rectfiles[i]).toString().split("\n").filter(x=>x.length).map(x=>x.split("\t").map(y=>parseInt(y)))
	r = r.filter(x=>(x[2]>0&&x[3]>0))


	var rr = []
	var kmax = r.length/180

	for (var kk = 0; kk < kmax; kk++){
		for (var ii = 0; ii < 9; ii++){
			for (var jj = 0; jj < 20; jj++){
				rr.push(r[-ii+jj*9+8+(kmax-1-kk)*180])
			}
		}
	}
	rects[nid]=rr
	imgfiles[nid]="../tmp/compact_pages/淮南鸿烈解.二十一卷.汉刘安撰.明茅坤.茅一桂辑评.明刊朱墨套印本 H"+nid+".png"
}


function displayImages(){
	for (var i = 1; i < imgfiles.length; i++){
		console.log(imgfiles[i])
	    var img = document.createElement('img');
	    img.src = imgfiles[i];
	    img.style.position = "absolute";
	    img.style.left = "100px"
	    img.style.width="900px"
	    img.style.top = (900*i)+"px"
	    document.body.appendChild(img);
	}
}
function displayRects(){


	ranges = []
	for (var i = 0; i < rects.length; i++){
		if (!rects[i]){
			ranges.push([rectdivs.length,rectdivs.length])
			continue
		}
		var ran = [rectdivs.length,rectdivs.length+rects[i].length]
		ranges.push(ran)

		var btn = document.createElement("button");
		btn.innerHTML = "Update page";
		btn.style.position = "absolute";
		btn.style.top = (i*900)+"px";
		btn.style.left = "140px";
		document.body.appendChild(btn);
		;;;(function (){
			var _ran = ran;
			btn.onclick = function(){
				// alert(_ran[0]+","+_ran[1])
				updateLabels(_ran[0],_ran[1]);
			};
		})()

		var jmp = document.createElement("button");
		jmp.innerHTML = i;
		jmp.style.position = "fixed";
		jmp.style.top = ((i%64)*15)+"px";
		jmp.style.left = (Math.floor(i/64)*20)+"px";
		jmp.style.width="20px"
		jmp.style.textAlign="left";
		jmp.style.padding="0px";
		jmp.style.fontSize="9px"
		document.body.appendChild(jmp);
		jmp.onclick = function(){
			// alert(this.innerHTML)
			var idx = parseInt(this.innerHTML)
			window.scrollTo(0,idx*900)
			updateLabels(ranges[idx][0],ranges[idx][1]);
			// alert(ranges[idx][0]+","+ranges[idx][1])
		}

		var lbl = document.createElement("div");
		lbl.innerHTML = i;
		lbl.style.position = "absolute";
		lbl.style.top = (900*i+30)+"px"
		lbl.style.left = "140px";
		lbl.style.fontSize="30px"
		lbl.style.color = "red";
		document.body.appendChild(lbl);

		for (var j = 0; j < rects[i].length; j++){
			var r = rects[i][j]

			var div = document.createElement("div");
			div.style.position = "absolute";
			div.style.left = (r[0]*0.15+100)+"px"
			div.style.top = (r[1]*0.15+i*900)+"px"
			div.style.width = (r[2]*0.15)+"px"
			div.style.height = (r[3]*0.15)+"px"
			div.style.border = "1px solid cyan";
			div.style.color = "red"
			div.style.zIndex="100"
			// div.innerHTML = "<div style='transform:translate(-10px,-5px)'>"+j+"</div>"
			document.body.appendChild(div);
			rectdivs.push(div);
		}
	}
	var atn = document.createElement("button");
	atn.innerHTML = "Update all";
	atn.style.position = "fixed";
	atn.style.top = "0px";
	atn.style.left = "230px";
	document.body.appendChild(atn);
	atn.onclick = function(){
		updateLabels();
	}
	atn.style.zIndex = "10000"


	var dtn = document.createElement("button");
	dtn.innerHTML = "Download text";
	dtn.style.position = "fixed";
	dtn.style.top = "0px";
	dtn.style.left = "800px";
	document.body.appendChild(dtn);
	dtn.onclick = function(){
		download("unocr-"+(new Date()).toString()+".txt",ta.value);
	}
	dtn.style.zIndex = "10000"

	var etn = document.createElement("button");
	etn.innerHTML = "Download map";
	etn.style.position = "fixed";
	etn.style.top = "0px";
	etn.style.left = "900px";
	document.body.appendChild(etn);
	etn.onclick = function(){
		var s = computeMap()
		console.log(s)
		saveData(s,"label-"+(new Date()).toString()+".txt");
	}
	etn.style.zIndex = "10000"

	console.log(ranges);
}

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

function computeMap(){
	var cnt = 0;
	var s = ""
	for (var i = 0; i < rects.length; i++){
		if (!rects[i]){
			continue
		}
		for (var j = 0; j < rects[i].length; j++){
			var name = `-H${i}-${rects[i][j].join("_")}.png`
			var val = rectdivs[cnt].innerHTML;
			s += name+"\t"+val+"\n"
			cnt ++;
		}
	}
	return s;
}



function updateLabels(i0,i1){

	var txt = document.getElementById("ta").value;
	if (i0 == undefined){
		i0 = 0;
	}
	if (i1 == undefined){
		i1 = txt.length;
	}
	var cnt = 0;
	for (var i = 0; i < txt.length; i++){
		if (txt[i] == "\n" || txt[i] == " "){
			continue;
		}
		if (txt[i] == "$"){
			var n = Math.ceil(cnt/20)*20-cnt;
			for (var j = 0; j < n; j++){
				if (i0 <= cnt && cnt < i1){
					rectdivs[cnt].innerHTML = "X";
				}
				cnt++;
			}
			continue;
		}
		if (txt[i] == "S"){
			var n = parseInt(txt[i+1]+txt[i+2]+txt[i+3]);
			for (var j = 0; j < n; j++){
				if (i0 <= cnt && cnt < i1){
					rectdivs[cnt].innerHTML = "X";
				}
				cnt++;
			}
			i += 3;
			continue;
		}
		if (txt[i] == "P"){
			for (var j = ranges.length-1; j >= 0; j--){
				if (ranges[j][0] < cnt){
					for (var k = cnt; k < ranges[j][1]; k++){
						rectdivs[k].innerHTML = "X";
						console.log(k)
					}
					// alert(cnt,ranges[j][1])
					cnt = ranges[j][1];

					break;
				}
			}
			i += 3;
			continue;
		}
		if (i0 <= cnt && cnt < i1){
			if (rectdivs[cnt]){
				if (rectdivs[cnt].innerHTML != txt[i]){
					rectdivs[cnt].innerHTML = txt[i]
				}
			}
		}
		cnt++;
	}
}

var html = `
<!--GENERATED FILE DO NOT EDIT-->
<head>
  <meta charset="UTF-8">
</head>
<style>
body{
	font-family: monospace;
}
#ta{
	position:fixed;
	left:1000px;
	top:0px;
	width: calc(100% - 1000px);
	height: 100%;
	font-size:15px;
	font-family:monospace;
}
</style>
<body>
<textarea id="ta">
</textarea>

<script>
	var txt = "${txt}";
	var ta = document.getElementById("ta")
	ta.innerText=txt;


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

	var rectdivs = []
	var imgfiles = ${JSON.stringify(imgfiles)};
	var rects=${JSON.stringify(rects)};
	
	var download = ${download.toString()}
	var displayImages = ${displayImages.toString()};
	var displayRects = ${displayRects.toString()};
	var updateLabels = ${updateLabels.toString()};
	var computeMap = ${computeMap.toString()}
	var ranges = []
	displayImages();
	displayRects();
	updateLabels();

</script>
</body>
`

fs.writeFileSync("../tmp/unocr.html",html)