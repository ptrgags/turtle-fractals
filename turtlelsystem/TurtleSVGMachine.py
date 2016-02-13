import math
from Machine import Machine

class TurtleSVGMachine(Machine):
    def __init__(self, origin_x=0, origin_y=0, width=1000, height=1000):
        super(TurtleSVGMachine, self).__init__()
        self.width = width
        self.height = height
        self.x = width / 2 + origin_x
        self.y = height / 2 - origin_y
        self.prompt_string = "turtle> "
        self.theta = 0
        self.pen = True
        self.path_d = "M {0} {1} ".format(self.x, self.y)
        self.opcodes = ["forward", "backward", "left", "right", "up", "down", "exit"]

    def forward(self, amount):
        try:
            r = float(amount)
            dx, dy = self.__polar_to_rect(r, self.theta)
            self.x += dx
            self.y += dy
            self.action = "l" if self.pen else "m"
            self.path_d += "{0} {1} {2} ".format(self.action, dx, dy)
            return "Turtle moved forward {0} units!".format(amount)
        except ValueError as e:
            return "usage: forward <amount>"

    def backward(self, amount):
        try:
            self.forward(-float(amount))
            return "Turtle moved backward {0} units!".format(amount)
        except ValueError as e:
            return "usage: backward <amount>"

    def left(self, amount):
        try:
            self.theta += float(amount)
            while self.theta > 360.0:
                self.theta -= 360.0
            return "Turtle turned left {0} degrees!".format(amount)
        except ValueError as e:
            return "usage: left <angle>"

    def right(self, amount):
        try:
            self.theta -= float(amount)
            while self.theta < 0.0:
                self.theta += 360.0
            return "Turtle turned right {0} units!".format(amount)
        except ValueError as e:
            return "usage: right <angle>"

    def up(self):
        self.pen = False
        return "Turtle lifted his pen!"

    def down(self):
        self.pen = True
        return "Turtle pressed his pen down onto the paper!"

    def __polar_to_rect(self, r, theta):
        x = r * math.cos(theta * math.pi / 180.0)
        y = -r * math.sin(theta * math.pi / 180.0)
        return x, y

    def __str__(self):
        return self.path_d

    @property
    def svg(self):
        return """
        <svg width="{0}" height="{1}">
            <path d="{2}" stroke="black" stroke-width="2" fill="none" />
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

if __name__ == "__main__":
    turtle = TurtleSVGMachine(0, 0)
    turtle.repl()
    print turtle.svg
