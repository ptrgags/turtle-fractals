from LSystem import LSystem

class TurtleCommands(object):
    """
    Generate Turtle commands for any TurtleMachine
    from an LSystem.
    """
    def __init__(self, data, iterations):
        """
        Constructor

        :param dict data: JSON data describing the fractal's
            L-System
        :param int iterations: iteration to generate
        """
        initiator = data['start']
        rules = data['rules']
        self.system = LSystem(initiator, rules)
        self.angle = data['angle']
        self.scale = 1.0 / data['divisor']
        self.initial_size = data['length']
        self.iterations = iterations

    def __iter__(self):
        """
        Generate turtle commands from the underlying
        L-System.

        :rtype: generator of str
        :returns: generator of turtle command strings
            in the form:
            OPCODE param1 param2 ...
        """
        size = self.initial_size * self.scale ** self.iterations
        steps = self.system.nth(self.iterations)
        for command in self.generate_commands(steps, self.angle, size):
            yield command

    def generate_commands(self, steps, angle, size):
        """
        Take an iteration of an LSystem and generate
        corresponding turtle commands

        :param str steps: Iteration string from the L-System.
        :param float angle: Angle for every turn left/right command.
        :param float size: Length of path for forward commands.

        :rtype: generator of str
        :returns: generator of turtle command strings
            in the form:
            OPCODE param1 param2 ...
        """
        for step in steps:
            if step in ["F", "A", "B"]:
                yield "forward {}".format(size)
            elif step == "+":
                yield "right {}".format(angle)
            elif step == "-":
                yield "left {}".format(angle)
            else:
                pass
