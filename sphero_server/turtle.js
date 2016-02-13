var readline = require("readline");
var sphero = require("sphero");
var orb = sphero("COM9");

var connected = false;
var noop = function(error, data){
	if (error)
	console.log(error);
	console.log("Data: " + data);
};

orb.connect(function () {
	console.log("Connected!");
	connected = true;
    orb.startCalibration(noop);
	setTimeout(function() {
		orb.finishCalibration(noop);
	}, 5000);
});

var rl = readline.createInterface({
	input: process.stdin,
  	output: process.stdout,
  	terminal: false
});

rl.on('line', function(line){
	if (connected) {
        if (line.match(/^forward/)) {
            var amount = parseInt(line.split(" ")[1]);
            forward(amount);
        }
        else if (line.match(/^backward/)) {
            var amount = parseInt(line.split(" ")[1]);
            backward(amount);
        }
        else if (line.match(/^left/)) {
            var angle = parseInt(line.split(" ")[1]); 
            left(angle);
        }
        else if (line.match(/^right/)) {
            var angle = parseInt(line.split(" ")[1]);
            right(angle);
        }
		else if (line.match(/^color/)) {
			var parts = line.split(" ")
			var red = parseInt(parts[1]);
			var green = parseInt(parts[2]);
			var blue = parseInt(parts[3]);
			color(red, green, blue);
		}
        else
            console.log("Not a valid command!");
        
	} else {
    	console.log("hold your horses! Sphero hasn't connected yet!");
	}
});

var theta = 0;

var forward = function(amount) {
    orb.roll(128, theta)
    setTimeout(function(){
        orb.stop();
    }, amount);
};

var backward = function(amount) {
    orb.roll(128, (theta + 180) % 360);
    setTimeout(function(){
        orb.stop();
    }, amount);
}

var left = function(amount) {
    theta -= amount;
    while (theta < 0)
        theta += 360;
    console.log(theta);
};

var right = function(amount) {
    theta = (theta + amount) % 360;
    console.log(theta);
};

var color = function(red, green, blue) {
	var c = {
		red: red & 0xFF,
		green: green & 0xFF,
		blue: blue & 0xFF
	}
	orb.setRgbLed(c, noop);
};
