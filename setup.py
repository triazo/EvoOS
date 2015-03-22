#! /usr/bin/python

import sys

if (len(sys.argv) == 2):
	if (sys.argv[1] == "test"):
		import evoos
		import evoos.test
		exit()



print "\tUsage: python setup.py [ test ]"
