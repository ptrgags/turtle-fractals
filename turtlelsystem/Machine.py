class Machine(object):
    """
    A Machine is any sort of class that
    takes instructions as strings:

    OPCODE param1 param2 ...

    opcodes are case insensitive,
    but the parametera may or may not be
    depending on how the subclass defines
    each command.

    Machines also come with a repl() method
    for making an interactive session.
    """
    def __init__(self):
        """
        :ivar prompt_string: the string for
            use in a REPL
        :ivar opcodes: the list of whitelisted
            commands. All others are ignored.
        """
        self.prompt_string = "command> "
        self.opcodes = ["exit"]
        self.running = True

    def do_command(self, command):
        """
        Run a command string, returning the result
        as a string. If any errors happen, they are
        currently returned as a string prefixed with
        "ERROR: "

        :param str command: Command string in the form
            "OPCODE param1 param2 ..." with 0 or more
            parameters depending on the command.

        :returns: The return value as a string or
            an error string
        :rtype: str
        """

        #Split the command into opcode and args
        parts = command.strip().split(" ")
        opcode = parts[0].lower()
        args = parts[1:]

        if opcode not in self.opcodes:
            return "ERROR: Command not found"

        try:
            func = getattr(self, opcode)
            return func(*args)
        except TypeError as e:
            return "ERROR: {}".format(e)

    def exit(self):
        """
        Exit the REPL

        :returns: Exit message
        :rtype: str
        """
        self.running = False
        return "Bye!"

    def repl(self):
        """
        Run a Read-Eval-Print Loop
        for this machine.
        """
        while self.running:
            command = raw_input(self.prompt_string)
            print(self.do_command(command))

if __name__ == "__main__":
    machine = Machine()
    machine.repl()
