THIS IS THE DEV BRANCH!!!!!

# EvoOs
the Electronic Voice Operated Operating System

Our plan...

##Have a central messaging core (EVOS MAIN)
     
listens for watchdog signals from modules, when a new one is received
sends initilize signal. This makes it redundant against EvoOS Main
going down briefly, as the initialize function should not reset it.

Location is decided by a dispatcher (see below), which will get a list
of possible listeners and their locations (how?), and decide which is
closest.  It then connects directly and sends the command via
module-module communication.

Most command things register three parts:
 - A command, probably put to a command interpreter such as julius or
 a console
 - Processing module, probably put onto the EvoOS main machine. There
 will be a module on that machine listening for module add events,
 which will pull the module code from the event source (via tcp
 address connectback) and start running it.



##Essential Event descriptions


###Initialize ()
    implemented on all modules on a standard port.  When recieved, a
    module should send any initilization events such as listening
    registering or julius grammar updates

###OnDeath (Nodeid)
   Event which EvoOS main stores for later and sends when it stops
   receiving pings from the modules that sends it. When a module
   receives this event, it should check if there are any module
   specific data stores for it (such as julius commands that require
   functionality of that module), and delete said data.

###JuliusGrammarUpdate(connectback)
   Listened for by the JuliusCompiler module. When recieved it will
   connect back to the port, and read the modifications to be made to
   the grammar tree over a custom protocol.

###JuliusGrammerUpdatePush(connectback)


##Essential Modules

###JuliusCompiler
   listens for database update events, and when one is recieved, it
