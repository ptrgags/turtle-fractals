readline = require "readline"
sphero = require "sphero"
net = require "net"

class SpheroTurtle
    constructor: (@port) ->
        console.log "Connecting to sphero..."
        @orb = sphero @port
        @connected = false
        @calibrated = false
        @busy = true
        @theta = 0
        @orb.connect @connect
        @orb.on 'error', @noop
        @client = null
        @command_queue = []

    connect: =>
        console.log "Connected!"
        @connected = true
        @orb.startCalibration @noop
        setTimeout @calibrate, 5000

    calibrate: =>
        @calibrated = true
        @orb.finishCalibration @continue_processing

    continue_processing: =>
        @busy = false
        @next_command()

    next_command: =>
        if @command_queue.length is 0
            console.log "Queue empty, wait for further commands"
        else
            while not @busy and @command_queue.length isnt 0
                command = @command_queue.shift()
                result = @do_command command
                console.log result

    add_command: (command) =>
        @command_queue.push command
        if not @connected
            @client.write "Woah there, Sphero's not ready yet! Command `#{command}`` was queued for later."
        else if not @calibrated
            @client.write "Patience my friend. Sphero is calibrating. Command `#{command}` was queued for later."
        else if @busy
            @client.write "Waiting for command to finish. Command `#{command}` was Queued for later."
        else
            @client.write "Running command `#{command}`..."
            @next_command()

    do_command: (command) =>
        [opcode, args...] = command.split(' ')
        switch opcode.toLowerCase()
            when "forward"
                [amount] = args
                amount = parseFloat amount
                if isNaN amount
                    return "ERROR: amount is NaN"
                @forward amount
            when "backward"
                [amount] = args
                amount = parseFloat amount
                if isNaN amount
                    return "ERROR: amount is NaN"
                @backward amount
            when "left"
                [angle] = args
                angle = parseFloat angle
                if isNaN angle
                    return "ERROR: angle is NaN"
                @left angle
            when "right"
                [angle] = args
                angle = parseFloat angle
                if isNaN angle
                    return "ERROR: angle is NaN"
                @right angle
            when "color"
                [red, green, blue] = args
                red = parseInt red
                green = parseInt green
                blue = parseInt blue
                if isNaN red
                    return "ERROR: red is NaN"
                if isNaN green
                    return "ERROR: green is NaN"
                if isNaN blue
                    return "ERROR: blue is NaN"
                @color red, green, blue
            else
                "ERROR: not a valid command"

    forward: (amount) =>
        @orb.roll 128, @theta
        @busy = true
        setTimeout @stop, amount
        "Sphero moved forward for #{amount / 1000.0} seconds"

    backward: (amount) =>
        angle = (@theta + 180) % 360
        @orb.roll 128, angle
        @busy = true
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
        @orb.setRgbLed c, @wait
        "Sphero changed color to rgb(#{c.red}, #{c.green}, #{c.blue})"

    stop: =>
        @orb.stop()
        @continue_processing()

    noop: (err, data) ->
        if err
            console.log err
        console.log "Data: #{JSON.stringify(data)}"

    wait: (err, data) =>
        if err
            console.log err
        else
            console.log "Data: #{JSON.stringify(data)}"
        @continue_processing()

sphero_turtle = new SpheroTurtle("COM9")

server = net.createServer (socket) ->
    socket.name = "#{socket.remoteAddress}:#{socket.remotePort}"
    socket.setEncoding("utf8")

    if sphero_turtle.client?
        socket.write "Sorry, first come first serve"
        socket.destroy()
        return
    else
        socket.write "Welcome #{socket.name}"
        sphero_turtle.client = socket

    socket.on 'end', ->
        sphero_turtle.client = null


    socket.on 'error', (error) ->
        if error.errno is "ECONNRESET"
            console.log "(Client #{socket.name} disconnected)"
        else
            console.log error
        sphero_turtle.client = null

    line_buffer = ''
    socket.on 'data', (data) ->
        line_buffer += data
        newline_index = line_buffer.indexOf '\n'
        while newline_index != -1
            line = line_buffer[...newline_index]
            sphero_turtle.add_command line
            line_buffer = line_buffer[newline_index+1...]
            newline_index = line_buffer.indexOf '\n'

server.listen 3000, '127.0.0.1'
