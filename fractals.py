import sys
import json
from turtlelsystem.LSystem import LSystem, LSystemOverflow
from turtlelsystem.TurtleMachine import TurtleMachine
from turtlelsystem.TurtleSVGMachine import TurtleSVGMachine

def iteration_commands(steps, angle, step_size):
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
    initial_size = data['length']

    system = LSystem(initiator, rules)
    try:
        steps = system.nth(iteration)
        size = initial_size * scale ** iteration
        return iteration_commands(steps, angle, size)
    except LSystemOverflow:
        print "ERROR: Too Many commands! Try a smaller iteration number"
        sys.exit(1)

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
        turtle = TurtleMachine(x, y)
    elif turtle_type == "svg":
        turtle = TurtleSVGMachine(x, y)

    for command in perform_iteration(iterations, data):
        turtle.do_command(command)

    if turtle_type == "turtle":
        turtle.freeze()
    elif turtle_type == "svg":
        with open("output.html", "wb") as f:
            f.write(turtle.html + "\n")
