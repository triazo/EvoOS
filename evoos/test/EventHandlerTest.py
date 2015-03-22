from ..EventHandler import EventHandler

e = EventHandler()
e.addListenerToEvent("I am a listener.", "I am an event.")

if (e.EventList["I am an event."] != set(["I am a listener."])):
	print "\n\nTEST FAILED"
	print e.EventList
	print "\n\n"
	raise SetError
