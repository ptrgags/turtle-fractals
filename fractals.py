import sys
import json
import argparse
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iterations", required=True, type=int,
        help="Number of iterations.")
    parser.add_argument("-f", "--input-file", required=True,
        help="Input JSON file that describes the fractal")
    parser.add_argument("-t", "--turtle-type", required=True,
        choices=['turtle', 'svg'], help="Type of turtle graphics output")
    args = parser.parse_args()

    with open(args.input_file, "rb") as f:
        data = json.loads(f.read())
        x = data.get('x', 0)
        y = data.get('y', 0)

    if args.turtle_type == "turtle":
        turtle = TurtleMachine(x, y)
    elif args.turtle_type == "svg":
        turtle = TurtleSVGMachine(x, y)

    for command in perform_iteration(args.iterations, data):
        turtle.do_command(command)

    if args.turtle_type == "turtle":
        turtle.freeze()
    elif args.turtle_type == "svg":
        with open("output.html", "wb") as f:
            f.write(turtle.html + "\n")
