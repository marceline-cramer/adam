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
    def __init__(self):
        # Default values
        self.wads = []
        self.iwad = "freedoom2.wad"
        self.process = None
        self.directory = './zandronum/'
        self.stdout = Queue()
        self.stderr = Queue()
        self.config = zandronum_config.ZandronumConfiguration(self.directory, self.echo)
    def start(self):
        if self.process:
            self.echo("Zandronum is already running.")
            return

        self.echo("Starting Zandronum...")
        # Start processing paramaters
        args = [self.directory + "zandronum-server"]

        args.append("-exec")
        args.append(self.config.load())

        args.append("-iwad")
        args.append(self.directory + self.iwad)

        # WADS/PK3s/etc.
        for wad in self.wads:
            args.append("-file")
            args.append(self.directory + wad)

        # Start the process
        self.echo("Parameters: `" + " ".join(args) + "`")
        self.process = Popen(args, bufsize=1, shell=False, universal_newlines=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)

        # Start threads and queues to monitor output from the process
        self.stdout_t = Thread(target=queue_output, args=(self.process.stdout, self.stdout))
        self.stderr_t = Thread(target=queue_output, args=(self.process.stderr, self.stderr))

        self.stdout_t.daemon = True
        self.stderr_t.daemon = True

        self.stdout_t.start()
        self.stderr_t.start()
    def isRunning(self):
        if self.process:
            return True
        else:
            return False
    def isReady(self):
        if self.isRunning() or not self.stdout.empty() or not self.stderr.empty():
            return True
        else:
            return False
    def getOutput(self):
        sout = []
        serr = []

        while not self.stdout.empty():
            sout.append(str(self.stdout.get_nowait()))

        while not self.stderr.empty():
            serr.append(str(self.stderr.get_nowait()))

        return (sout, serr)
    def send(self, message):
        if self.process:
            self.echo("Sending: " + message)
            self.process.stdin.write(message + '\n')
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
    def addWad(self, wad):
        if wad not in self.wads:
            self.wads.append(wad)
    def echo(self, message):
        self.stdout.put_nowait(message + '\n')
        print("\033[94m {}\033[00m" .format(message))
