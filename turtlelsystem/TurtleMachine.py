import turtle
from Machine import Machine

class TurtleMachine(Machine):
    def __init__(self, origin_x, origin_y):
        super(TurtleMachine, self).__init__()
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        turtle.colormode(255)
        self.turtle.up()
        self.turtle.setpos(origin_x, origin_y)
        self.turtle.down()
        self.prompt_string = "turtle> "
        self.opcodes = [
            "forward",
            "backward",
            "left",
            "right",
            "up",
            "down",
            "color",
            "move",
            "exit"
        ]

    def freeze(self):
        """
        Freeze the screen when done.
        """
        turtle.done()

    def forward(self, amount):
        try:
            self.turtle.forward(float(amount))
            return "Turtle moves forward {} units!".format(amount)
        except ValueError:
            return "usage: forward <amount>"

    def backward(self, amount):
        try:
            self.turtle.backward(float(amount))
            return "Turtle moves backward {} units!".format(amount)
        except ValueError:
            return "usage: backward <amount>"

    def left(self, amount):
        try:
            self.turtle.left(float(amount))
            return "Turtle turns left {} degrees!".format(amount)
        except ValueError:
            return "usage: left <angle>"

    def right(self, amount):
        try:
            self.turtle.right(float(amount))
            return "Turtle turns right {} degrees!".format(amount)
        except ValueError:
            return "usage: right <angle>"

    def up(self):
        self.turtle.up()
        return "Turtle lifts his pen!"

    def down(self):
        self.turtle.down()
        return "Turtle lowers his pen to the paper!"

    def color(self, red, green, blue):
        try:
            self.turtle.pencolor(int(red), int(green), int(blue))
            "Turtle changes color to rgb({}, {}, {})!".format(red, green, blue)
        except ValueError:
            return "usage: color <red> <green> <blue>"

    def move(self, x, y):
        try:
            self.turtle.setpos(float(x), float(y))
            "Turtle moves to ({}, {})!".format(x, y)
        except ValueError:
            return "usage: move <x> <y>"

if __name__ == "__main__":
    machine = TurtleMachine(0, 0)
    machine.repl()
