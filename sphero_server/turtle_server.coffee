readline = require "readline"
sphero = require "sphero"
#TODO: Don't hardcode this!
orb = sphero "COM9"

connected = false
theta = 0

noop = (error, data) ->
    if error
        console.log error
    console.log "Data: #{data}"

orb.connect ->
    console.log "Connected!"
    connected = true
    orb.startCalibration noop
    setTimeout ->
        orb.finishCalibration noop
    , 5000

rl = readline.createInterface
    input: process.stdin
    output: process.stdout
    terminal: false

rl.on 'line', (line) ->
    if connected
        [opcode, args...] = line.trim().split " "
        switch opcode.toLowerCase()
            when "forward"
                [amount] = args
                amount = parseInt amount
                forward amount
            when "backward"
                [amount] = args
                amount = parseInt amount
                backward amount
            when "left"
                [angle] = args
                angle = parseInt angle
                left angle
            when "right"
                [angle] = args
                angle = parseInt angle
                right angle
            when "color"
                [red, green, blue] = args
                red = parseInt red
                green = parseInt green
                blue = parseInt blue
                color red, green, blue
            else
                console.log "not a valid command!"
    else
        console.log "hold your horses! Sphero hasn't connected yet!"

forward = (amount) ->
    orb.roll 128, theta
    setTimeout ->
        orb.stop();
    , amount

backward = (amount) ->
    orb.roll 128, (theta + 180) % 360;
    setTimeout ->
        orb.stop();
    , amount

left = (amount) ->
    theta -= amount;
    while theta < 0
        theta += 360;
    console.log theta

right = (amount) ->
    theta = (theta + amount) % 360;
    console.log theta

color = (red, green, blue) ->
	c =
		red: red & 0xFF
		green: green & 0xFF
		blue: blue & 0xFF
	orb.setRgbLed c, noop
