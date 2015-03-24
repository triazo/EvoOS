#!/usr/bin/python3

import threading
import socket
import struct
import json
import time

import module
from util.error import errorlog


"""
Implementation of the EvoOS main node, aka the central relay, as a module
"""

class EvoOSMainModule():
    def __init__(self, umid):
        self.umid = umid
        self.pingtime = time.time()

    def update(self, pingtime):
        self.pingtime = pingtime
        

class EvoOSMain(EvModule):
    """Class for encapsulating the main evoos relay module"""

    # Watchdog thread keeps track of which clients are connected
    watchdog_thread = threading.Thread()
            
    # Data structure storing event listeners
    dispatcher      = eh.EventHandler()
            
    # Dictionary of currently connected modules
    connected_mods  = {}
    mod_number = 1
    
    def __init__(self):
        """Initializer for the EvoOS main moudule"""
        pass

    def watchdog(self):
        """Starts a watchdog listening on the port passend as a parameter of
        the function, which will keep track of which modules are
        connected.  Should be run in another thread by calling the
        helper function"""
        # Create a socket to listen on
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', port))
        
        while True:
            data, addr = s.recvfrom(1024)
            # The module id is sent in the first 16 bytes of the watchdog
            # Everything else is ignored
            
            if not module_id in connected_mods:
                self.init_submodule(module_id)
                continue
            else:
                connected_mods[module_id].update(time.time())
                            
                        

    def init_submodule(self, module_id):
        """Will call the initilize submodule event on the module
        to be run when a new module connects"""

        # The module id is currently addressing information on how to
        # connect back
        module_ip = socket.inet_ntoa(module_id[:4])
        module_port = struct.unpack_from("!H", module_id, offset=4)

        # Connect 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((module_ip, module_port))
        except OSError as e:
            errorlog("Failed to connect back to module at %s:%d: %s"%(module_ip, module_port, str(e)))
            return
        
        # And send the init module event
        message = json.dumps({"event":"init_module","umid": self.mod_number})
        
        s.write(struct.pack("!I", len(message))
        s.write(message)

        s.close()

        # If it got to this point without crashing, add it to the module list
        connect_mods[module_id] = EvoOSMainModule(self.mod_number)
        self.mod_number += 1
        
        
                
    def start_dispatcher(self, port=51101):
        self.dispatcher.startDispatcher()
        
        
        
    def start_watchdog(self, port=51100):
        """Starts a watchdog on the given port in a new thread"""

        # Define the watchdog thread and start it
        self.watchdog_thread = threading.Thread(name="Watchdog",
                                                target=self.watchdog,
                                                kwargs={"port": 51100})
        self.watchdog_thread.start()
        


if __name__ == "__main__":
    evoosmain = EvoOSMain()
    evoosmain.start_watchdog(port=51100)
    evoosmain.start_dispatcher(port=51101)
    
