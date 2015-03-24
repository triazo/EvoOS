#! /usr/bin/python

import json
import socket
import struct
from util.network import notifyEvent
from util.error import ErrorLog
from util.event import digestEvent

"""
    Event Handler

    Basic event utility programs to be run by EvoOS main.
    Port 51101 - Event listener port.

    On creation, all modules register for which events they would like.
    UID's 16byte string (16 characters, lets go ascii).
"""

#I'm assuming there is an error file called self.ErrorLogger.


class EventHandler:
    EventList = dict();
    EventSocket = 0;

    #--Functions------------

    def addListenerToEvent(self, lid, eid):
        if (eid in self.EventList.keys()):
            if (lid not in self.EventList[eid]):    
                self.EventList[eid].add([lid])

            else:
                #Umm, somehow the same module tried to register twice, weird...
                self.ErrorLogger.write("EventHander: RegError Looks like {0} tried to register {1} which it was already registered for.".format(lid, eid))

        else:
            #Event doesn't exist, create it's list of listeners.
            self.EventList[eid] = set([lid])


        
    def removeListenerFromEvent(self, lid, eid):    
        if (eid in self.EventList.keys()):
            if (lid not in self.EventList[eid]):    
                self.EventList[eid].remove(lid)

                #Quickly double check the event is still important, remove it from the dictionary otherwise.
                if (not len(self.EventList[eid])):
                    del self.EventList[eid]

            else:
                #Umm, somehow the same module tried to register twice, weird...
                self.ErrorLogger.write("EventHander: unRegError {0} tried to unregister {1} which it was not regisered for.".format(lid, eid))

        else:
            #Event doesn't exist...
            self.ErrorLogger.write("EventHander: unRegError {0} tried to unregister {1} which does not exist.".format(lid, eid))



    def triggerEvent(self, eid, meta):
        #Notifies listeners registered to the specific event.
        if (eid in self.EventList.keys()):
            for module in self.EventList[eid]:
                notifyEvent(module, meta)

        else:    
            #Event doesn't have any listeners.
            self.ErrorLogger.write("EventHander: TriggerEvent {0} was called but has no listeners.".format(eid))



    
    def receivedEvent(self, event):
        #Called when routines recieves a connection/event call.
        #Check to see if it is one of our two special events, addListener, removeListener.
        #TODO: Seperate permissions so one module can't remove all others.

        #Eid = event type, meta = plain text of original event.
        eid, meta, lid, cbeid = digestEvent(event)

        if (eid == "addListener"):
            self.addListenerToEvent(lid, cbeid) 

        elif (eid == "removeListener"):
            self.removeListenerToEvent(lid, cbeid) 
        
        else:
            self.triggerEvent(eid, meta)



    def startDispatcher(self):
        EventSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        EventSocket.bind(("", 51101))
        EventSocket.listen(10)

        #Block and listen for requests, should probably spawn a new thread but since out other modules are threaded I can block here.

        while True:
            #Forward messages as soon as they come in.
            #TODO: Make it difficult for messages to have a rediculus message stream that clogs the message list.
            
            respSocket, senderIP = EventSocket.accept()

            mesgFirst = respSocket.recv(4)            
            #DEBUG3
            #print "Recived four bytes:", mesgFirst

            mesgLength = int(struct.unpack("!I", mesgFirst)[0])
            #DEBUG2
            #print "Message {0}".format(mesgLength)
 
            meta = struct.unpack("!{0}s".format(mesgLength), respSocket.recv(mesgLength))[0]
            #DEBUG2
            #print "Received message of length {0}: {1}".format(mesgLength, meta)
            
            self.receivedEvent(meta)
            respSocket.close()
      

 
    def __del__(self):
        self.EventSocket.close() 

    def __init__(self):
        self.EventList = dict()
