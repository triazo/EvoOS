#!/usr/bin/python2

import signal
import sys
import os
import subprocess
import pyjulius

PORT=51099

def startJulius():
    # TODO: Capture stdout for synchro and logging

    # TODO: Julius mic detection is pretty bad. Have read waveform
    # from stdin and do mic detection manually
    jProcess = subprocess.Popen(['/usr/bin/julius',
                                      '-C', 'evJulius.conf',
                                      '-nolog', '-quiet',
                                      '-module', str(PORT)])
    # TODO: pause and wait for julius to become fully up
    jClient = pyjulius.Client('localhost', PORT)
    return (jProcess, jClient)


def stopJulius(jProcess, jClient):
    jProcess.terminate()
    jClient.stop()

    jProcess.wait()
    jClient.join()

    jClient.disconnect()

def listenLoop(jClient):
    result = jClient.results.get(False)
    if isinstance(result, pyjulius.Sentence):
        print("sentence '%s' recognized with score %.2f" % (result, result.score))


def safeStop():
    stopJulius()

def main():
    signal.signal(signal.SIGINT, safeStop)
