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
	ctx.lineWidth = 13;
}

//font_style = font
function set_text_Style(font_style, font_color) {
	ctx.font = font_style;
	ctx.fillStyle = font_color;
}

function set_canvas_styles() {
	set_canvas();
	set_text_Style("15px Helvetica", "#000000")
}

eel.expose(draw_point);
function draw_point(coordinates, r) {
	ctx.beginPath(); //Start path
	ctx.arc(coordinates[0], coordinates[1], r, 0, Math.PI * 2, true); // Draw a point using the arc function of the canvas with a point structure.
	ctx.fillStyle = "#50504e";
    ctx.fill();
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

eel.expose(clear_canvas);
function clear_canvas() {
	ctx.clearRect(0, 0, c.width, c.height);
}

function draw_map() {
	eel.draw_map()();	
}

eel.expose(add_name);
function add_name(station, ang, coordinates){
	ctx.save();

	ctx.translate(coordinates[0], coordinates[1]);
	ctx.rotate(ang * Math.PI);

	ctx.textAlign = 'left';
	ctx.fillText(station, 0, 0);

	ctx.restore();
}

async function helloo() {

	ctx.lineWidth = 11;
	ctx.lineJoin = "round";
	
	ctx.beginPath();
	
	/*ctx.moveTo(0,0);
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
	*/
	//Writes dist...

	var from = document.getElementById("from").value;
	var to = document.getElementById("to").value;
	
	let ret = await eel.a_star_search(from, to)();
	console.log(ret[0]);

}
