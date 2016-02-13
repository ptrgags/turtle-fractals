readline = require "readline"
sphero = require "sphero"
net = require "net"

class SpheroTurtle
    constructor: (@port) ->
        console.log "Connecting to sphero..."
        @orb = sphero @port
        @connected = false
        @calibrated = false
        @theta = 0
        @orb.connect @connect
        @orb.on 'error', @noop

    connect: =>
        console.log "Connected!"
        @connected = true
        @orb.startCalibration @noop
        setTimeout @calibrate, 5000

    calibrate: =>
        @calibrated = true
        @orb.finishCalibration @noop

    do_command: (command) =>
        if not @connected
            "Hold your horses! Sphero isn't connected yet!"
        else if not @calibrated
            "Patience, my friend. Sphero likes to calibrate in peace."
        else
            [opcode, args...] = command.split(' ')
            switch opcode.toLowerCase()
                when "forward"
                    [amount] = args
                    amount = parseInt amount
                    @forward amount
                when "backward"
                    [amount] = args
                    amount = parseInt amount
                    @backward amount
                when "left"
                    [angle] = args
                    angle = parseInt angle
                    @left angle
                when "right"
                    [angle] = args
                    angle = parseInt angle
                    @right angle
                when "color"
                    [red, green, blue] = args
                    red = parseInt red
                    green = parseInt green
                    blue = parseInt blue
                    @color red, green, blue
                else
                    "ERROR: not a valid command"

    forward: (amount) =>
        @orb.roll 128, @theta
        setTimeout @stop, amount
        "Sphero moved forward for #{amount / 1000.0} seconds"

    backward: (amount) =>
        angle = (@theta + 180) % 360
        @orb.roll 128, angle
        setTimeout @stop, amount
        "Sphero moved backward for #{amount / 1000.0} seconds"

    left: (amount) =>
        @theta -= amount
        while @theta < 0
            @theta += 360
        "Sphero turned #{amount} degrees to the left. Current Heading: #{@theta} degrees"

    right: (amount) =>
        @theta = (@theta + amount) % 360
        "Sphero turned #{amount} degrees to the right. Current Heading: #{@theta} degrees"

    color: (red, green, blue) ->
        c =
            red: red & 0xFF
            green: green & 0xFF
            blue: blue & 0xFF
        @orb.setRgbLed c, @noop
        "Sphero changed color to rgb(#{red}, #{green}, #{blue})"

    stop: =>
        @orb.stop()

    noop: (err, data) ->
        if err
            console.log err
        console.log "Data: #{JSON.stringify(data)}"

sphero_turtle = new SpheroTurtle("COM9")

server = net.createServer (socket) ->
    socket.name = "#{socket.remoteAddress}:#{socket.remotePort}"
    socket.setEncoding("utf8")

    if client?
        socket.write "Sorry, first come first serve"
        socket.destroy()
        return
    else
        socket.write "Welcome #{socket.name}"
        client = socket

    socket.on 'end', ->
        client = null

    socket.on 'error', (error) ->
        if error.errno is "ECONNRESET"
            console.log "(Client #{socket.name} disconnected)"
        else
            console.log error
        client = null

    line_buffer = ''
    socket.on 'data', (data) ->
        line_buffer += data
        newline_index = line_buffer.indexOf '\n'
        while newline_index != -1
            line = line_buffer[...newline_index]
            result = sphero_turtle.do_command(line)
            console.log result
            socket.write result
            line_buffer = line_buffer[newline_index+1...]
            newline_index = line_buffer.indexOf '\n'

server.listen 3000, '127.0.0.1'
