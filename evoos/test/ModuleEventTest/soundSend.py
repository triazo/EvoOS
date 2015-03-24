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



class sendAudio:
    audioPort = 0
    
    def startAudioStream(self):
        print "Starting audio stream."
        wf = open("evoos/test/ModuleEventTest/house_lo.wav", 'rb')
        p = pyaudio.PyAudio()
 
        data = wf.read(1024)
        while data != '':
            self.audioPort.sendall(data)
            data = wf.read(1024)
        
        p.terminate()
        wf.close()




    def logIntoEvoOS(self):
        event = {}
        event["event"] = "startStream" #cbied is the event we are adding a listener to
        event["host"] = "127.0.0.1"
        event["port"] = 4002
        sendEvent(event)



    def waitForStream(self):
        respSocket, senderIP = self.audioPort.accept()
        print "Sender got conection."
        self.oldPort = self.audioPort
        self.audioPort = respSocket 



    def run(self):
        #Set up our listening port.
        self.audioPort = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audioPort.bind(("", 4002))
        self.audioPort.listen(5)

        self.logIntoEvoOS()

        while True:
            self.waitForStream()
            self.startAudioStream()
            self.audioPort.close()
            self.audioPort = self.oldPort


    def __del__(self):
        self.audioPort.close()
        self.oldPort.close()
