#! /usr/bin/python

import sys

if (len(sys.argv) == 2):
    if (sys.argv[1] == "test"):
        import evoos
        import evoos.test.EventHandlerTest
        exit()

    elif (sys.argv[1] == "send"):
        import evoos.test.ModuleEventTest
        exit()

    elif (sys.argv[1] == "run"):
        from evoos.EventHandler import EventHandler
        from evoos.util.error import ErrorLog
        e = EventHandler()
        e.ErrorLogger = ErrorLog()
        print "Starting EvoOS."
        e.startDispatcher() 
        exit()

print "\tUsage: python setup.py [ test | send | run ]"
