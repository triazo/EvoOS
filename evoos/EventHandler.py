#! /usr/bin/python

import json
from util.network import notifyEvent
from util.error import ErrorLog

"""
	Event Handler

	Basic event utility programs to be run by EvoOS main.
	Port 51101 - Event listener port.

	On creation, all modules register for which events they would like.
	UID's 16byte string (16 characters, lets go ascii).
"""

#I'm assuming there is an error file called ErrorFile.


class EventHandler:
	EventList = dict();

	#--Functions------------

	def addListenerToEvent(self, lid, eid):
		if (eid in self.EventList.keys()):
			if (lid not in self.EventList[eid]):	
				self.EventList[eid].add(lid)

			else:
				#Umm, somehow the same module tried to register twice, weird...
				ErrorFile.write("EventHander: RegError Looks like {0} tried to register {1} which it was already regisered for.".format(lid, eid))

		else:
			#Event doesn't exist, create it's list of listeners.
			self.EventList[eid] = set(lid)


		
	def removeListenerFromEvent(self, lid, eid):	
		if (eid in self.EventList.keys()):
			if (lid not in self.EventList[eid]):	
				self.EventList[eid].remove(lid)

				#Quickly double check the event is still important, remove it from the dictionary otherwise.
				if(not len(self.EventList[eid])):
					del self.EventList[eid]

			else:
				#Umm, somehow the same module tried to register twice, weird...
				ErrorFile.write("EventHander: unRegError {0} tried to unregister {1} which it was not regisered for.".format(lid, eid))

		else:
			#Event doesn't exist...
			ErrorFile.write("EventHander: unRegError {0} tried to unregister {1} which does not exist.".format(lid, eid))



	def triggerEvent(self, eid, meta):
		#Notifies listeners registered to the specific event.
		if (eid in self.EventList.keys()):
			for (module in self.EventList[eid]):
				notifyEvent(eid, meta)

		else:	
			#Event doesn't have any listeners.
			ErrorFile.write("EventHander: TriggerEvent {0} was called but has no listeners.".format(eid))



	
	def recievedEvent(self, eid, meta)
		#Called when routines recieves a connection/event call.
		#Check to see if it is one of our two special events, addListener, removeListener.
		#TODO: Seperate permissions so one module can't remove all others.

		if (eid == "addListener"):
			pass		

		elif (eid == "removeListener"):
			pass
		
		else:
			triggerEvent(eid, meta)



	def startDispacher(self):
		#self.listenForEvents()
		pass


	def __init__(self):
		self.EventList = dict()
