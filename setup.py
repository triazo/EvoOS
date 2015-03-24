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

print "\tUsage: python setup.py [ test ]"
