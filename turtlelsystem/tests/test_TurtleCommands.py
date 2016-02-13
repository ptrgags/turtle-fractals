from nose.tools import raises
from turtlelsystem.TurtleCommands import TurtleCommands
from turtlelsystem.LSystem import LSystemOverflow

GOOD_DATA = {
    "x": -300,
    "y": -200,
    "angle": 60,
    "length": 600,
    "divisor": 3,
    "start": "F",
    "rules": {
        "F": "F+F--F+F"
    }
}

GOOD_COMMANDS = [
    ["FORWARD", "LEFT", "LEFT", "FORWARD", "LEFT", "LEFT", "FORWARD"],
    ["FORWARD", "RIGHT", "FORWARD", "LEFT", "LEFT", "FORWARD", "RIGHT", "FORWARD"]
]

@raises(ValueError)
def test_invalid_iterations():
    commands = TurtleCommands(GOOD_DATA, -1)

@raises(ValueError)
def test_empty_data():
    commands = TurtleCommands({}, 1)

def test_nth():
    def trial(n):
        commands = TurtleCommands(GOOD_DATA, n)
        for command, expected in zip(commands, GOOD_COMMANDS[n]):
            assert command.split(" ")[0] == expected

    for i in xrange(2):
        yield trial(i)

@raises(LSystemOverflow)
def test_overflow():
    commands = TurtleCommands(GOOD_DATA, 100)
    for command in commands:
        pass
