net = require "net"

clients = []

server = net.createServer (socket) ->
    socket.name = "#{socket.remoteAddress}:#{socket.remotePort}"
    clients.push socket

    socket.write "Welcome #{socket.name}"

    socket.on 'end', ->
        clients.splice clients.indexOf(socket), 1

    socket.on 'data', (data) ->
        console.log data.toString()

server.listen 3000, '127.0.0.1'
