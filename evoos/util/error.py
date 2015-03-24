import sys

class ErrorLog:
    lastMessage = ""
    def write(self, msg):
        self.lastMessage = msg
        self.out.write("\t")
        self.out.write(msg)
        self.out.write("\n")

    def __init__(self, pipe=sys.stdout):
        self.out = pipe

    def __del__(self):
        self.out.close()
