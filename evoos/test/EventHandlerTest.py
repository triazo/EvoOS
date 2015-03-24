"""
    Testing code for EventHandler
"""

from ..EventHandler import EventHandler
from ..util.error import ErrorLog

import thread
import time
import socket
import pipes
import json

e = EventHandler()


#--addListener test.
e.addListenerToEvent("I am a listener.", "I am an event.")
e.ErrorLogger = ErrorLog(pipe=pipes.Template().open("/dev/null", "w"))

if (e.EventList["I am an event."] != set(["I am a listener."])):
	print "\n\nTEST FAILED"
	print e.EventList
	print "\n\n"
	raise SetError

print "addListener Test PASSED"



#--Event receive test.
def startDispatch(e):
    e.startDispatcher()

#Send sample data.
def sendSampleData(msg):
    def sendData(msg):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 51101))
        s.sendall(msg)
        s.close()
    
    thread.start_new_thread(sendData, (msg,))

#Was having some issues making threads behave when it can to output.
thread.start_new_thread(startDispatch, (e,))
time.sleep(.05) #Give it a second for the other thread to setup the socket listener.
sendSampleData('\x00\x00\x00\x29{"event":"test", "info":"I am a thingy."}')

"""
#A quick test to see threading output.
def dummyPrint():
    while True:
        print "HI!"
#thread.start_new_thread(dummyPrint, ())
"""

time.sleep(.1) #Wait for a while to let the above event occur.
if (e.ErrorLogger.lastMessage != "EventHander: TriggerEvent test was called but has no listeners."):
    print "\n\nTEST FAILED"
    raise TriggerMessageError

print "eventTrigger Test 1 PASSED"




#--Event addListener Test
eventCallback = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
eventCallback.bind(("", 4001))
eventCallback.listen(5)

event = {}
event["event"] = "addListener"
event["lid"] = "127.0.0.1:4001"
event["cbeid"] = "test" #cbied is the event we are adding a listener to
msg = json.dumps(event)
msg = 3*chr(0)+chr(len(msg))+msg
sendSampleData(msg)

#----IMPORTANT!-----
time.sleep(.1) #Wait for message to send!

if (e.EventList["test"] != set(["127.0.0.1:4001"])):
	print "\n\nTEST FAILED"
	print e.EventList
	print "\n\n"
	raise SetError

print "Event addListener Test PASSED"



#--Event triggerEvent Test

"""
    This test is a little tricky, we'll setup our event packet,
    start a new thread to process the response we'll get from EvoOS main,
    then send out packet, wait a bit until we should have gotten a response.
"""

event = {}
event["event"] = "test"
event["payload"] = "This is some sample meta data."
msg = json.dumps(event)
msg = 3*chr(0)+chr(len(msg))+msg

passed = False

def waitForResponse(msg, s):
    global passed
    r, ip = s.accept()
    m = r.recv(len(msg))
    r.close()
    if (m == msg[4:]):
        passed = True

#thread.start_new_thread(sendSampleData, (msg,)
thread.start_new_thread(waitForResponse, (msg, eventCallback))
#waitForResponse(passed, msg, eventCallback)

time.sleep(.1)
sendSampleData(msg)
time.sleep(.1)

if (not passed):
	print "\n\nTEST FAILED"
	print e.EventList
	print "\n\n"
	raise TriggerEventError

print "Event trigger PASSED"

eventCallback.close()
