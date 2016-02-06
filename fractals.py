import sys
import json
from turtlebots import TurtleRobot, TurtleSVG

initiator = "F--F--F"
rules = {
    "F": "F+F--F+F"
}
angle = 60
initial_size = 600
scale = 1.0 / 3.0
MAX_STEPS = 100000

def iterate(initiator, rules, iterations):
    output = initiator
    for i in xrange(iterations):
        next_iteration = ""
        for ch in output:
            if ch in rules:
                next_iteration += rules[ch]
            else:
                next_iteration += ch
        output = next_iteration
    return output

def iteration_commands(steps, angle, step_size):
    if len(steps) > MAX_STEPS:
        print "Error: desired steps: {} Maximum steps: {}".format(len(steps), MAX_STEPS)
        return
    for step in steps:
        if step in ["F", "A", "B"]:
            yield "forward {}".format(step_size)
        elif step == "+":
            yield "right {}".format(angle)
        elif step == "-":
            yield "left {}".format(angle)
        else:
            pass

def perform_iteration(iteration, data):
    initiator = data['start']
    rules = data['rules']
    angle = data['angle']
    scale = 1.0 / data['divisor']
    size = data['length']

    steps = iterate(initiator, rules, iteration)
    size = initial_size * scale ** iteration
    return iteration_commands(steps, angle, size)

if __name__ == '__main__':
    try:
        iterations = int(sys.argv[1])
        input_file = sys.argv[2]
        turtle_type = sys.argv[3].lower()
    except (ValueError, IndexError):
        print "Usage: turtleDrawer.py <iterations> <file> <turtle|svg>"
        sys.exit(1)

    with open(input_file, "rb") as f:
        data = json.loads(f.read())
        x = data.get('x', 0)
        y = data.get('y', 0)

    if turtle_type == "turtle":
        turtle = TurtleRobot(x, y)
    elif turtle_type == "svg":
        turtle = TurtleSVG(x, y)

    for command in perform_iteration(iterations, data):
        turtle.do_command(*command.split(' '))

    if turtle_type == "turtle":
        turtle.freeze()
    elif turtle_type == "svg":
        with open("output.html", "wb") as f:
            f.write(turtle.html + "\n")
