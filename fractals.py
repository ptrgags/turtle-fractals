import sys
import json
import argparse
from turtlelsystem.LSystem import LSystem, LSystemOverflow
from turtlelsystem.TurtleCommands import TurtleCommands
from turtlelsystem.TurtleMachine import TurtleMachine
from turtlelsystem.TurtleSVGMachine import TurtleSVGMachine
from turtlelsystem.SpheroTurtleMachine import SpheroTurtleMachine

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--iterations", required=True, type=int,
        help="Number of iterations.")
    parser.add_argument("-f", "--input-file", required=True,
        help="Input JSON file that describes the fractal")
    parser.add_argument("-t", "--turtle-type", required=True,
        choices=['turtle', 'svg', 'sphero'], help="Type of turtle graphics output")
    args = parser.parse_args()

    with open(args.input_file, "rb") as f:
        data = json.loads(f.read())
        x = data.get('x', 0)
        y = data.get('y', 0)

    if args.turtle_type == "turtle":
        turtle = TurtleMachine(x, y)
    elif args.turtle_type == "svg":
        turtle = TurtleSVGMachine(x, y)
    elif args.turtle_type == 'sphero':
        turtle = SpheroTurtleMachine()

    commands = TurtleCommands(data, args.iterations)
    for command in commands:
        turtle.do_command(command)

    if args.turtle_type == "turtle":
        turtle.freeze()
    elif args.turtle_type == "svg":
        with open("output.html", "wb") as f:
            f.write(turtle.html + "\n")
