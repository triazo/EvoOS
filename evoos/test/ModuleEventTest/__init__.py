"""
    A test of EvoOS event handling.
    
    A set of test modules that connect to EvoOS, and use it to negotiate a direct stream.
"""

from ...EventHandler import EventHandler
import soundSend
import soundReceive
import thread
from ...util.error import ErrorLog
import time

print "Starting Dispatcher."

def startSending():
    sender = soundSend.sendAudio()
    sender.run()

def startReceiving():
    receive = soundReceive.receiveAudio()
    receive.run()

def startDispatcher():
    e = EventHandler()
    e.ErrorLogger = ErrorLog()
    e.startDispatcher()

print "Preforming Module Test."
thread.start_new_thread(startDispatcher, ())
time.sleep(.1)
thread.start_new_thread(startReceiving, ())
time.sleep(.1)
thread.start_new_thread(startSending, ())

while raw_input() != "END":
    pass
