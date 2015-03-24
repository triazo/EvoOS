#A simple way to play a raw wav stream.
#Modified to act as an EvoOS module.

import pyaudio
import wave
import sys
import socket
import json    
import struct


#Send sample data.
def sendEvent(e):
    msg = json.dumps(e)

    #I'll add the code to do the right thing later.
    assert(len(msg) < 255)
    msg = 3*chr(0)+chr(len(msg))+msg

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 51101))
    s.sendall(msg)
    s.close()



class receiveAudio:
    host = ""
    port = ""
    EventPort = 0
    
    def startAudioStream(self):
        # instantiate PyAudio (1)
        p = pyaudio.PyAudio()
        
        # open stream (2)
        """
            This is important, the below values need to be replaced with those particular to the file.
            I'm working on a simple protocol to send these but have been too lazy to actually make it as for now.
        """
        stream = p.open(format=p.get_format_from_width(1), channels=1, rate=11025, output=True)
        print "Attempting to connect to {0}:{1}".format(self.host, self.port) 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((str(self.host), self.port))
        print "Receiver Has Connected"
        data = s.recv(1024)
        
        while data != '':
            stream.write(data)
            data = s.recv(1024)
        
        # stop stream (4)
        stream.stop_stream()
        stream.close()
        s.close()
        print "Done streaming."
        
        # close PyAudio (5)
        p.terminate()



    def logIntoEvoOS(self):
        event = {}
        event["event"] = "addListener"
        event["lid"] = "127.0.0.1:4001"
        event["cbeid"] = "startStream" #cbied is the event we are adding a listener to
        sendEvent(event)
 


    def waitForStream(self):
        respSocket, senderIP = self.EventPort.accept()
        mesgFirst = respSocket.recv(4)
        mesgLength = int(struct.unpack("!I", mesgFirst)[0])
        meta = struct.unpack("!{0}s".format(mesgLength), respSocket.recv(mesgLength))[0]
        respSocket.close() 
        
        event = json.loads(meta) 
        self.host = event["host"]
        self.port = int(event["port"])
        print "Received Audio Request From: {0}:{1}".format(self.host, self.port)



    def run(self):
        #Set up our listening port.
        self.EventPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.EventPort.bind(("", 4001))
        self.EventPort.listen(5)

        self.logIntoEvoOS()

        while True:
            self.waitForStream()
            self.startAudioStream()

    def __del__(self):
        self.EventPort.close()
