net = require 'net'

client = new net.Socket
client.connect 3000, '127.0.0.1', ->
    console.log 'Connected'
    client.write 'Hi there!'

client.on 'data', (data) ->
    console.log data.toString()
    client.destroy()

client.on 'close', ->
    console.log 'Connection closed.'
