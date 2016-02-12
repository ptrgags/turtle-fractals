import math
from Machine import Machine

class TurtleSVGMachine(Machine):
    def __init__(self, origin_x, origin_y, width=1000, height=1000):
        super(TurtleSVGMachine, self).__init__()
        self.width = width
        self.height = height
        self.x = width / 2 + origin_x
        self.y = height / 2 - origin_y
        self.prompt_string = "turtle> "
        self.theta = 0
        self.pen = True
        self.path_d = "M {} {} ".format(self.x, self.y)
        self.opcodes = ["forward", "backward", "left", "right", "up", "down", "exit"]

    def forward(self, amount):
        try:
            r = float(amount)
            dx, dy = self.__polar_to_rect(r, self.theta)
            self.x += dx
            self.y += dy
            self.action = "l" if self.pen else "m"
            self.path_d += "{} {} {} ".format(self.action, dx, dy)
            return "Turtle moved forward {} units!".format(amount)
        except ValueError as e:
            return "usage: forward <amount>"

    def backward(self, amount):
        try:
            self.forward(-float(amount))
            return "Turtle moved backward {} degrees!".format(amount)
        except ValueError as e:
            return "usage: backward <amount>"

    def left(self, amount):
        try:
            self.theta += float(amount)
            return "Turtle turned left {} degrees!".format(amount)
        except ValueError as e:
            return "usage: left <angle>"

    def right(self, amount):
        try:
            self.left(-float(amount))
            return "Turtle turned right {} units!".format(amount)
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

if __name__ == "__main__":
    turtle = TurtleSVGMachine(0, 0)
    turtle.repl()
    print turtle.svg
