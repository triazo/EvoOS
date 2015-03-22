#A simple way to play a raw wav stream.

import pyaudio
import wave
import sys
import socket


host = 'graphene.triazo.net'
port = 8080
chunk = 1024

# instantiate PyAudio (1)
p = pyaudio.PyAudio()


# open stream (2)
"""
    This is important, the below values need to be replaced with those particular to the file.
    I'm working on a simple protocol to send these but have been too lazy to actually make it as for now.
"""
stream = p.open(format=p.get_format_from_width(2), channels=2, rate=44100, output=True)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
data = s.recv(chunk)

while data != '':
    stream.write(data)
    data = s.recv(chunk)


# stop stream (4)
stream.stop_stream()
stream.close()
s.close()

# close PyAudio (5)
p.terminate()
