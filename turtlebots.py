import turtle
import sys
import math

class Robot(object):

    def __init__(self):
        self.prompt_string = "command> "
        self.commands = ["exit"]
        self.running = True

    def do_command(self, command, *args):
        if command in self.commands:
            try:
                return getattr(self, command)(*args)
            except TypeError as e:
                print e
        else:
            print "Command not found"

    def exit(self):
        self.running = False

    def repl(self):
        while self.running:
            command = raw_input(self.prompt_string).split(" ")
            result = self.do_command(command[0], *command[1:])
            if result:
                print result


class TurtleRobot(Robot):
    def __init__(self, origin_x, origin_y):
        super(TurtleRobot, self).__init__()
        self.turtle = turtle.Turtle()
        self.turtle.speed(0)
        self.turtle.up()
        self.turtle.setpos(origin_x, origin_y)
        self.turtle.down()
        self.prompt_string = "turtle> "
        self.commands = [
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
        turtle.done()

    def forward(self, amount):
        try:
            self.turtle.forward(float(amount))
        except ValueError:
            return "usage: forward <amount>"

    def backward(self, amount):
        try:
            self.turtle.backward(float(amount))
        except ValueError:
            return "usage: backward <amount>"

    def left(self, amount):
        try:
            self.turtle.left(float(amount))
        except ValueError:
            return "usage: left <angle>"

    def right(self, amount):
        try:
            self.turtle.right(float(amount))
        except ValueError:
            return "usage: right <angle>"

    def up(self):
        self.turtle.up()

    def down(self):
        self.turtle.down()

    def color(self, red, green, blue):
        try:
            self.turtle.pencolor(int(red), int(green), int(blue))
        except ValueError:
            return "usage: color <red> <green> <blue>"

    def move(self, x, y):
        try:
            self.turtle.setpos(float(x), float(y))
        except ValueError:
            return "usage: move <x> <y>"

class TurtleSVG(Robot):
    def __init__(self, origin_x, origin_y, width=1000, height=1000):
        super(TurtleSVG, self).__init__()
        self.width = width
        self.height = height
        self.x = width / 2 + origin_x
        self.y = height / 2 - origin_y
        self.prompt_string = "turtle> "
        self.theta = 0
        self.pen = True
        self.path_d = "M {} {} ".format(self.x, self.y)
        self.commands = ["forward", "backward", "left", "right", "up", "down", "exit"]

    def forward(self, amount):
        try:
            r = float(amount)
            dx, dy = self.__polar_to_rect(r, self.theta)
            self.x += dx
            self.y += dy
            self.action = "l" if self.pen else "m"
            self.path_d += "{} {} {} ".format(self.action, dx, dy)
            return str(self)
        except ValueError as e:
            return "usage: forward <amount>"

    def backward(self, amount):
        try:
            self.forward(-float(amount))
        except ValueError as e:
            return "usage: backward <amount>"

    def left(self, amount):
        try:
            self.theta += float(amount)
        except ValueError as e:
            return "usage: left <angle>"

    def right(self, amount):
        try:
            self.left(-float(amount))
        except ValueError as e:
            return "usage: right <angle>"

    def up(self):
        self.pen = False

    def down(self):
        self.pen = True

    def __polar_to_rect(self, r, theta):
        x = r * math.cos(theta * math.pi / 180.0)
        y = -r * math.sin(theta * math.pi / 180.0)
        return x, y

    def __str__(self):
        return self.path_d

    @property
    def svg(self):
        return """
        <svg width="{}" height="{}">
            <path d="{}" stroke="black" stroke-width="2" fill="none" />
        </svg>
        """.format(self.width, self.height, self.path_d)

    @property
    def html(self):
        return """
        <html>
        <body>
            {}
        </body>
        </html>
        """.format(self.svg)
