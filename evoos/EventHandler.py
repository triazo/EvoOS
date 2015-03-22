#! /usr/bin/python

import json

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


	def __init__(self):
		self.EventList = dict()
