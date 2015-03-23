import socket

def notifyEvent(ip, meta):
    sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender.connect(decodeIP(ip))
    sender.sendall(meta)
    sender.close()

def decodeIP(ip):
    #I'm assuming all ip's are IPv4 for now.
    assert(ip.count(":") == 1)
    rval = ip.split(":")
    rval[0] = str(rval[0])
    rval[1] = int(rval[1])
    return tuple(rval)
