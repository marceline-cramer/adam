#!/usr/bin/python3

import asyncio
import os
from queue import Queue, Empty
from threading import Thread
from subprocess import Popen, PIPE, TimeoutExpired

import zandronum_config

# Grabs output from a pipe and adds it to the queue
def queue_output(out, queue):
    for line in iter(out.readline, ''):
        queue.put("> "+line)
    out.close()

class Zandronum:
    def __init__(self, directory=None, iwad=None, port=None):
        # Default values
        self.wads = []
        self.process = None

        # Set port
        if not port:
            self.port = 10666
        else:
            self.port = port
        self.echo("Serving Zandronum on port "+str(self.port))

        # Set the directory
        if not directory:
            self.echo("Zandronum directory defaulting to ./zandronum/")
            self.directory = './zandronum/'
        else:
            if os.path.exists(directory):
                self.directory = directory
                self.echo("Using "+directory+" as Zandronum directory")
            else:
                self.echo("Invalid directory "+directory+". Defaulting to ./zandronum/")
                self.directory = './zandronum/'

        # Locate the server binary
        linuxBinary = os.path.join(self.directory, "zandronum-server")
        windowsBinary = os.path.join(self.directory, "zandronum-server.exe")
        if os.path.exists(linuxBinary):
            self.executablePath = linuxBinary
        elif os.path.exists(windowsBinary):
            self.executablePath = windowsBinary
        else:
            self.echo("Zandronum server binary not found.")
            raise RuntimeError("Zandronum server binary not found.")
        self.echo("Using server executable "+self.executablePath)

        # Set the IWAD
        if not iwad:
            self.echo("Defaulting to IWAD freedoom2")
            iwadPath = os.path.join(self.directory, "freedoom2.wad")
            if os.path.exists(iwadPath):
                self.iwad = "freedoom2.wad"
            else:
                self.echo(iwadPath+" was not found. Aborting.")
                raise RuntimeError("Missing IWAD freedoom2.wad")
        else:
            iwadPath = os.path.join(self.directory, iwad)
            if os.path.exists(iwadPath):
                self.iwad = iwadPath
                self.echo("Using "+iwadPath+" as IWAD")
            else:
                self.echo("IWAD "+iwadPath+" does not exist. Aborting.")
                raise RuntimeError("Missing IWAD")

        self.stdout = Queue()
        self.stderr = Queue()

        self.config = zandronum_config.ZandronumConfiguration(self.directory, self.echo)
    def start(self):
        if self.process:
            self.echo("Zandronum is already running.")
            return

        self.echo("Starting Zandronum...")

        # Start processing parameters
        args = [self.executablePath]

        args.append("-exec")
        args.append(self.config.load())

        args.append("-port")
        args.append(str(self.port))

        args.append("-iwad")
        args.append(self.iwad)

        # WADS/PK3s/etc.
        for wad in self.wads:
            args.append("-file")
            args.append(self.directory + wad)

        # Start the process
        self.echo("Parameters: `" + " ".join(args) + "`")
        self.process = Popen(args, bufsize=1, shell=False, universal_newlines=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)

        # Start threads and queues to monitor output from the process
        # Yes, it's ugly.
        self.stdout_t = Thread(target=queue_output, args=(self.process.stdout, self.stdout))
        self.stderr_t = Thread(target=queue_output, args=(self.process.stderr, self.stderr))

        self.stdout_t.daemon = True
        self.stderr_t.daemon = True

        self.stdout_t.start()
        self.stderr_t.start()

    # Checks if the process is active
    def isRunning(self):
        if self.process:
            return True
        else:
            return False

    # If the server is running OR we still have output to dump,
    # Zandronum needs to still be treated as active
    def isReady(self):
        if self.isRunning() or not self.stdout.empty() or not self.stderr.empty():
            return True
        else:
            return False

    # Dump the queues
    def getOutput(self):
        sout = []
        serr = []

        while not self.stdout.empty():
            sout.append(str(self.stdout.get_nowait()))

        while not self.stderr.empty():
            serr.append(str(self.stderr.get_nowait()))

        return (sout, serr)

    # Send a string to the server process
    def send(self, message):
        if self.process:
            self.echo("Sending: " + message)
            self.process.stdin.write(message + '\n')

    # Shut down the process and close threads
    def shutDown(self):
        if self.process:
            if self.process.returncode != None:
                self.process = None
                self.echo("Zandronum has crashed.")
            else:
                self.echo("Shutting down Zandronum...")
                os.system("kill " + str(self.process.pid))
                self.process = None
            self.echo("Joining threads...")
            self.stdout_t.join()
            self.stderr_t.join()
            self.echo("Stopped successfully.")
        else:
            self.echo("Zandronum is already stopped.")

    # Add a wad
    # duh
    def addWad(self, wad):
        if wad not in self.wads:
            self.wads.append(wad)

    # Print a colored output message
    def echo(self, message):
        if self.isRunning():
            self.stdout.put_nowait(message + '\n')
        print("\033[94m {}\033[00m" .format(message))
