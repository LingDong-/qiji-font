
var name_eq_main = typeof require !== 'undefined' && require.main === module;


module.exports = async function (){

	const fs = require('fs')
	const { createCanvas, loadImage } = require('canvas')
	var root = "../"

	var chars = ["字"]
	var labels = Object.fromEntries(fs.readFileSync(root+"data/labels_all.txt").toString().split("\n").filter(x=>x.length).map(x=>[x.split("\t")[1],x.split("\t")[0].replace(".png",".svg")]))

	var W = 100;
	var masks = [];

	var glyphs = chars.map(x=>fs.readFileSync(root+"output/stage/"+labels[x]).toString())
	for (var i = 0; i < glyphs.length; i++){
		var btoa = x=>Buffer.from(x).toString('base64')
		var svg64 = 'data:image/svg+xml;base64,'+btoa(glyphs[i]);
		var img = await loadImage(svg64);

		var canv = createCanvas(W,W);
		var ctx = canv.getContext('2d')
		ctx.drawImage(img,0,0);
		var dat = ctx.getImageData(0,0,100,100).data
		var mask = []
		for (var j = 0; j < dat.length; j+=4){
			mask[j/4]=dat[j+3]//(dat[j+3]>128)*255
		}
		masks.push(mask)
	}
	
	function main(){
		var is_node = typeof requestAnimationFrame == 'undefined';
		var W = 100;

		var canv;
		if (is_node){
			const { createCanvas } = require('canvas')
			var fs = require('fs')
			canv = createCanvas(W,W);
		}else{
			var div = document.createElement("div");
			var liv = document.createElement("div");

			canv = document.createElement("canvas");
			canv.width=W;
			canv.height=W;
			canv.style.border = "1px solid black";
			liv.appendChild(canv)

			var loading = document.createElement("div");
			loading.innerHTML = "LOADING..."
			loading.style.fontFamily="monospace"
			loading.style.width = "100px";
			loading.style.textAlign="center"
			liv.appendChild(loading);

			
			liv.style.position="absolute";
			liv.style.left="calc(50% - 50px)";
			liv.style.top="calc(50% - 80px)";

			div.appendChild(liv);
			div.style.position="absolute";
			div.style.left="0px";
			div.style.top="0px";
			div.style.width="100%";
			div.style.height="100%";
			div.style.background="rgba(255,255,255,0.8)"
			div.style.zIndex="100"
			document.body.appendChild(div);
		}

		var ctx = canv.getContext("2d")
		
		var head = [0,W,1];
		var parts = []
		var idx = 0;

		var killed = false;
		function kill(){
			killed = true;
		}

		var frame = -1;

		if (typeof requestAnimationFrame == 'undefined'){
			requestAnimationFrame = function(x){
				
				var dat = ctx.getImageData(0,0,W,W).data;
				var ok = false;
				for (var i = 0; i < dat.length; i++){
					if (dat[i] != 0){
						ok = true;
						break;
					}
				}
				if (ok && (frame % 4 == 3)){
					frame++;
					console.log(frame/4);
					fs.writeFileSync(`../tmp/loader/${(frame/4).toString().padStart(5,"0")}.png`, canv.toBuffer())
				}else{
					if (ok){
						frame++;
					}
				}
				setTimeout(x,0)
			}
		}
		function a_pour(){
			
			if (killed){
				if (!is_node){
					document.body.removeChild(div);
				}
				return;
			}
			var mask = masks[idx];

			if (parts.length == 0){
				var z = mask[head[1]*W+head[0]];

				ctx.clearRect(head[0]-head[2],0,1,head[1]-1);
				if (z > 0){
					ctx.fillStyle=`rgba(0,0,0,${z})`
					ctx.fillRect(head[0],0,1,head[1]);
				}
				head[0]+=head[2]
				if (head[0]>=W || head[0] < 0){
					head[2] *= -1;
					head[1] -= 1;
				}
				if (head[1] <= 0){
					head = [0,W,1];
					for (var i = 0; i < mask.length; i++){
						if (mask[i]>128){
							var t = (i%W)/W;
							var s = Math.cos(t*10)+1//+(1.5*Math.floor(i/W)/W);
							parts.push([i%W,Math.floor(i/W),0,s*Math.random()*3+3])
						}
					}
					if (is_node){
						idx=idx + 1;
					}else{
						idx=(idx+1)%masks.length;
					}
					setTimeout(a_pour,300);
				}else if (z == 0 || head[0] % 5 != 0){
					a_pour();
				}else{
					requestAnimationFrame(a_pour);
				}
			}else{
				
				ctx.clearRect(0,0,W,W);
				ctx.fillStyle="black";
				for (var i = parts.length-1; i >= 0; i--){
					parts[i][0]+=parts[i][2];
					parts[i][1]+=parts[i][3];
					ctx.fillRect(parts[i][0],parts[i][1],1,1);
					if (parts[i][1] > W){
						parts.splice(i,1);
					}
				}
				if (parts.length == 0 && idx>=masks.length){
					return;
				}else{
					requestAnimationFrame(a_pour);
				}
			}
		}
		a_pour();
		return kill;
	}
	return `
		var masks = ${JSON.stringify(masks)};
		var killLoader = (${main.toString()})();
	`
}



if (name_eq_main){(async ()=>{
	var src = await module.exports()
	// console.log(src)
	eval(src);
})();}



