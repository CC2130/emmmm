#!/usr/bin/env python3
# encoding : utf-8
# Filename: daemonprocess.py
__author__ = 'Jia Chao'

import os
import sys
import time
from signal import SIGTERM
from singlelock import SingleLock

class DaemonProcess ():
    '''
    Extends by son class, run as service in system
    '''
    def __init__ (self):
        '''
        You don't care this
        '''
        self.lockfile = '/var/run/daemonprocess.lock'
        pass

    def _locking (self, action=1):
        '''
        action == 0, free lock
        action == 1, add lock
        action == 2, get the pid from lockfile
        '''
        # if not self.lockfile, named one as program name
        try:
            if self.lockfile:
                lockfile = self.lockfile
        except Exception as e:
            name = os.path.splitext (os.path.basename (sys.argv[0]))[0] + '.lock'
            lockfile = '/var/run/' + name

        # lock work
        lock = SingleLock (lockfile)
        if action == 0:
            lock.free ()
        if action == 1:
            return lock.lock ()
        if action == 2:
            try:
                with open (lockfile, 'r') as f:
                    pid, name = f.read ().split ('\n')[:2]
                    return int (pid)
            except Exception as e:
                return

        return True

    def _kill_process (self):
        pid = self._locking (2)
        if not pid:
            return

        try:
            while True:
                os.kill (pid, SIGTERM)
                time.sleep (0.1)
        except OSError as err:
            err = str (err)
            if err.find ('No such process') > 0:
                pass
            else:
                print (err)
                sys.exit (1)

    def start (self):
        '''
        Run as daemon service
        '''
        self._daemonize ()

        # lock and run after daemonize
        if not self._locking (1):
            return
        self.run ()
        pass

    def stop (self):
        '''
        stop service
        '''
        self._kill_process ()
        self._locking (0)
        pass

    def restart (self):
        '''
        restart service
        '''
        self.stop ()
        self.start ()
        pass

    def _daemonize (self):
        '''
        Double fork, process adopted by init
        '''
        try:
            pid = os.fork ()
            if pid > 0:
                # exit first parent
                sys.exit (0)
        except OSError as e:
            logging.error ("fork #1 failed: %d (%s)" % (e.errno, e,strerror))
            # excit from second parent
            sys.exit (1)
        # decouple from parent environment
        os.chdir ("/")
        os.setsid ()
        os.umask (0)

        # do second fork
        try:
            pid = os.fork ()
            if pid > 0:
                sys.exit (0)
        except OSError as e:
            logging.error ("fork #1 failed: %d (%s)" % (e.errno, e,strerror))
            sys.exit (1)

    def run (self):
        '''
        SonClass rewrite:
        here do something
        '''
        pass

class Demo (DaemonProcess):
    def __init__ (self):
        self.lockfile = '/var/run/hahademo.pid'
        pass

    def run (self):
        time.sleep (20)

if __name__ == '__main__':
    help (DaemonProcess)
    #d = Demo ()
    # run in front
    #d.run ()
    # run as daemon service
    #d.start ()
