import turtle

t = turtle.Turtle()
turtle.colormode(255)
turtle.bgcolor(0, 0, 0)
t.speed("fastest")
t.up()
t.setpos(-300, -200)
t.down()

initiator = [
    ["color", 0, 255, 255],
    ["fwd", 600],
    ["left", 120],
    ["fwd", 600],
    ["left", 120],
    ["fwd", 600],
    ["left", 120],
]


'''
initiator = [
    ["color", 0, 255, 255],
    ["fwd", 600],
    ["left", 90],
    ["fwd", 600],
    ["left", 90],
    ["fwd", 600],
    ["left", 90],
    ["fwd", 600],
    ["left", 90]
]
'''

def run(t, prgm):
    for instruction in prgm:
        opcode = instruction[0]
        data = instruction[1:]
        if opcode == "fwd":
            t.forward(data[0])
        elif opcode == "bwd":
            t.backward(data[0])
        elif opcode == "left":
            t.left(data[0])
        elif opcode == "right":
            t.right(data[0])
        elif opcode == "color":
            t.pencolor(*data)

def generator(init):
    for instruction in init:
        opcode = instruction[0]
        data = instruction[1:]
        if opcode == "fwd":
            a = data[0] / 3.0
            yield ["fwd", a]
            yield ["right", 60]
            yield ["fwd", a]
            yield ["left", 120]
            yield ["fwd", a]
            yield ["right", 60]
            yield ["fwd", a]
        elif opcode == "color":
            color = data[:]
            color[0] += 40
            if color[0] > 255:
                color[0] = 255
            yield ["color"] + color
        else:
            yield instruction
            
    
step = initiator

for i in range(6):
    #t.clear()
    run(t, step)
    step = [x for x in generator(step)]

turtle.done()
        
