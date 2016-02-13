net = require "net"

client = null

do_something = (line) ->
    console.log line
    return "Command successful"

server = net.createServer (socket) ->
    socket.name = "#{socket.remoteAddress}:#{socket.remotePort}"
    socket.setEncoding("utf8")

    if client?
        socket.write "Sorry, first come first serve"
        socket.destroy()
        return
    else
        client = socket

    socket.write "Welcome #{socket.name}"

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
            result = do_something line
            socket.write result
            line_buffer = line_buffer[newline_index+1...]
            newline_index = line_buffer.indexOf '\n'

server.listen 3000, '127.0.0.1'
