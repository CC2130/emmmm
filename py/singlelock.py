#!/opt/py3.6/ve1/bin/python3
# encoding : utf-8
# Filename: SingleLock.py

import os
import sys
import psutil

class SingleLock ():
    '''
    Some work can only keep one process alive in system
    '''
    def __init__ (self, lockfile='/var/run/SingleLock.pid'):
        self.pid = os.getpid ()
        self.lockfile = lockfile
        self.name = os.path.basename (sys.argv[0])

    def lock (self):
        '''
        First check lock status, if not locked,
        try to add a new lock then return True
        Notice that it will store the main process name and it's pid in lockfile
        '''
        # check lock status
        if not self.check_lock ():
            return False

        with open (self.lockfile, 'w') as f:
            f.write (str (self.pid)+'\n'+self.name)

        return True

    def free (self):
        '''
        Release lock and remove lockfile
        '''
        if os.access (self.lockfile, os.R_OK):
            try:
                os.remove (self.lockfile)
            except Exception as e:
                pass

    def check_lock (self):
        '''
        Check lock:
            Is lockfile exists?
            Is this pid still running?
            Is the process name tally with the name record in lockfile?
        If not locking, return True
        '''
        if os.access (self.lockfile, os.R_OK):
            with open (self.lockfile, 'r') as f:
                old_pid, old_name = f.read ().split ('\n')[:2]
                if psutil.pid_exists (int (old_pid)):
                    if psutil.Process (int (old_pid)).name () == old_name:
                        return False
                else:
                    os.remove (self.lockfile)

        return True
