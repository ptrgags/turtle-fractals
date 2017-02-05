import socket
from turtlelsystem.Machine import Machine

class SpheroTurtleMachine(Machine):
    ADDR = ('localhost', 3000)
    def __init__(self):
        super(SpheroTurtleMachine, self).__init__()
        self.connect()
        self.prompt_string = "sphero> "
        self.opcodes = [
            "forward",
            "backward",
            "left",
            "right",
            "color",
            "exit"
        ]

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.connect(self.ADDR)
            ack = self.socket.recv(8192)
        except socket.error as e:
            raise RuntimeError("Could not connect to sphero server! Error: {0}".format(e))

        if ack.startswith("Sorry"):
            raise RuntimeError("Connection rejected by server.")
        else:
            print("Connected!")

    def send_message(self, message):
        try:
            self.socket.sendall("{0}\n".format(message))
            return self.socket.recv(8192)
        except socket.error:
            raise RuntimeError("Whoops! something went wrong with the server connection")

    def forward(self, amount):
        return self.send_message("FORWARD {0}".format(amount))

    def backward(self, amount):
        return self.send_message("BACKWARD {0}".format(amount))

    def left(self, amount):
        return self.send_message("LEFT {0}".format(amount))

    def right(self, amount):
        return self.send_message("RIGHT {0}".format(amount))

    def color(self, red, green, blue):
        return self.send_message("COLOR {0} {1} {2}".format(red, green, blue))

if __name__ == "__main__":
    machine = SpheroTurtleMachine()
    machine.repl()
