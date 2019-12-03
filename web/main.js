var is_from_ok = false;
var is_to_ok = false;

async function is_valid_from(){
	
	var from = document.getElementById("from").value;
	let is_station = await eel.is_station(from)();

	if (from == ''){
		document.getElementById("from").style.border = "none";
		is_from_ok = false;
		document.getElementById("subButton").disabled = true;
	}
	else if (is_station){
		document.getElementById("from").style.border = "thick solid rgb(0, 204, 0)";
		is_from_ok = true;
		document.getElementById("subButton").disabled = !(is_from_ok && is_to_ok);
	}
	else{
		document.getElementById("from").style.border = "thick solid #FF0000";
		is_from_ok = false;
		document.getElementById("subButton").disabled = true;
	}
}

async function is_valid_to(){
	
	var to = document.getElementById("to").value;
	let is_station = await eel.is_station(to)();

	if (to == ''){
		document.getElementById("to").style.border = "none";
		is_to_ok = false;
		document.getElementById("subButton").disabled = true;
	}
	else if (is_station){
		document.getElementById("to").style.border = "thick solid rgb(0, 204, 0)";
		is_to_ok = true;
		document.getElementById("subButton").disabled = !(is_from_ok && is_to_ok);
	}
	else{
		document.getElementById("to").style.border = "thick solid #FF0000";
		is_to_ok = false;
		document.getElementById("subButton").disabled = true;
	}
}

var c;
var ctx;

function set_canvas() {
	c = document.getElementById("myCanvas");
	ctx = c.getContext("2d");
}

//font_style = font
function set_text_Style(font_style, font_color) {
	ctx.font = font_style;
	ctx.fillStyle = font_color;
}

function set_canvas_styles() {
	set_canvas();
	set_text_Style("30px Arial", "white")
}

eel.expose(move_to);
function move_to(coordinates) {
	ctx.beginPath();
	ctx.moveTo(coordinates[0], coordinates[1]);
}

eel.expose(draw_line_to);
function draw_line_to(coordinates) {
	ctx.lineTo(coordinates[0], coordinates[1]);
}

eel.expose(set_line_color);
function set_line_color(color) {
	ctx.strokeStyle = color;
	ctx.stroke();
}

eel.expose(put_text);
function put_text(text, coordinates) {
	ctx.fillText(text, coordinates[0], coordinates[1]);
}


async function helloo() {

	ctx.lineWidth = 13;
	ctx.lineJoin = "round";
	
	ctx.beginPath();
	
	ctx.moveTo(0,0);
	ctx.lineTo(1000,600);
	ctx.lineTo(0, 600);
	ctx.lineTo(1000, 0);

	ctx.strokeStyle = '#65a15e';
	ctx.stroke();
	
	ctx.beginPath();

	ctx.moveTo(0,0);
	ctx.lineTo(300,300);

	ctx.strokeStyle = '#ffffff';
	ctx.stroke();

	ctx.beginPath();

	ctx.moveTo(300,300);
	ctx.lineTo(400,400);
	
	ctx.strokeStyle = '#00ffff';
	ctx.stroke();

	//Writes dist...
	ctx.font = "30px Arial";
	ctx.fillStyle = "white";
	ctx.fillText("dist",400,400);

	var from = document.getElementById("from").value;
	var to = document.getElementById("to").value;
	var n = document.getElementById("n").value;
	let ret = await eel.say_hello_py(from, to, n)();
	console.log(ret[0]);

}
