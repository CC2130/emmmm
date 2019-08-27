#!/usr/bin/env python3
# encoding : utf-8
# Filename: tarball.py

import os
import sys
import tarfile

class Tarball ():
    '''
    You can use this Tarball to create or extract a tarfile
    Example:
        tar = Tarball ()
        # to backup /etc
        tar.tar ('/etc/', '/bak/My_etc_backup.tar.gz', True)
        # recover /etc
        tar.extract ('/bak/My_etc_backup.tar.gz', '/')
    '''
    def __init__ (self):
        '''
        You don't care this
        '''
        self.tarball = ''
        self.tardir = ''
        self.path = ''
        self.abspath = None

    def tar (self, path, tarball, abspath=False):
        '''
            path :    the path you want to create tarball
            tarball : target tarfile name
            abspath : default is False, use relative path
                        if True, use abspath from '/'
        '''
        self.tarball = tarball
        self.tardir = os.path.basename (tarball).rsplit ('.tar', 1)[0]
        self.path = os.path.abspath (path)
        self.abspath = abspath
        try:
            tar = tarfile.open (self.tarball, "w:gz")
            for root, dirs, files in os.walk (path):
                for f in files:
                    abspath = os.path.join (root, f)
                    if self.abspath:
                        tar.add (abspath)
                    else:
                        relative_path = abspath.replace (self.path, self.tardir)
                        tar.add (abspath, relative_path)

            tar.close ()
        except Exception as e:
            logging.error (e)
            return False
        return True
        pass

    def extract (self, tarball, path=''):
        '''
        tarball: the source tarball's path
        path:    the target extract path, default is the tarball's path
        '''
        self.tarball = tarball
        if path == '':
            self.path = os.path.dirname (tarball)
        else:
            self.path = path

        try:
            tar = tarfile.open (self.tarball)
            file_names = tar.getnames ()
            for fname in file_names:
                tar.extract (fname, self.path)

            tar.close ()
            pass
        except Exception as e:
            logging.error (e)
            return False

if __name__ == '__main__':
    help (Tarball)
    pass
