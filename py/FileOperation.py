#!/usr/bin/env python3
# encoding : utf-8
# Filename: FileOperation
__author__ = 'Jia Chao'

#################################################################################
#                               Say somthing ?                                  #
#################################################################################

import os
import sys
import stat
import shutil

DMODE = 0o644

class FileOperation ():
    def __init__ (self):
        self.path = ''
        self.ori_file = ''
        self.dest_file = ''
        self.plist = []
        self.deep = 0
        pass

    def get_info (self, path):
        pass

    def mkfile (self, path):
        if os.path.exists (path):
            return

        _dir = os.path.dirname (path)
        if os.path.isdir (_dir):
            self.mkdir (_dir)

        try:
            os.mknod (path, 0o644)
        except Exception as e:
            raise

    def copy (self, src, dest):
        # check src file
        if not self.normal_check (src):
            return

        if os.path.isdir (dest):
            _basename = os.path.basename (src)
            dest = os.path.join (dest, _basename)
        else:
            _dir = os.path.dirname (dest)
            self.mkdir (_dir)

        try:
            shutil.copytree (src, dest)
        except Exception as e:
            raise

    def move (self, src, dest):
        # check src file
        if not self.normal_check (src):
            return

        if not os.path.isdir (dest):
            _dir = os.path.dirname (dest)
            self.mkdir (_dir)

        try:
            shutil.move (src, dest)
        except Exception as e:
            raise
        pass

    def remove (self, path):
        try:
            if os.path.isdir (path):
                shutil.rmtree (path)
            else:
                os.remove (path)
        except Exception as e:
            raise

    def mkdir (self, path):
        if os.path.isdir (path):
            return

        try:
            os.makedirs (path, 0o755)
        except Exception as e:
            raise

    def listdir (self, path, ftype=0, deep=0, abspath=True):
        '''
            ftype = 0, all files & dirs
            ftype = 1, all files
            ftype = 2, all dirs

            deep = 0, find the deepest files
        '''
        self._listdirs (path, _ftype=ftype, _deep=deep, _abspath=abspath, start=True)

        return self.plist
        pass

    def _listdirs (self, path, _ftype=0, _deep=0, _abspath=True, start=False):
        if start:
            self.path = path
            self.deep = _deep
            _deep = 0

        _deep += 1
        if _abspath:
            def collect (path): self.plist.append (os.path.abspath (path))
        else:
            def collect (path): self.plist.append (path)

        for item in os.listdir (path):
            fflag = True
            cpath = os.path.join (path, item)
            if os.path.isdir (cpath):
                fflag = False
                if self.deep == 0 or _deep < self.deep:
                    self._listdirs (cpath, _ftype, _deep, _abspath)

            if _ftype != 0:
                if (_ftype == 1 and not fflag) or (_ftype == 2 and fflag):
                    continue

            collect (cpath)

    def normal_check (self, path):
        # file is accessable & regular
        if not self.accessable (src):
            raise FileExistsError ('file not accessable')
            return False
        if not self.isregular (src):
            raise FileExistsError ('not a regular file')
            return False

        return True

    def accessable (self, path):
        if os.path.exists (path):
            if os.access (path, os.R_OK):
                if self.islinking (path):
                    return True

        return False

    def islinking (self, path):
        # not link file, True
        if not os.path.islink (path):
            return True

        # check link source is available
        _realpath = os.path.realpath (path)
        return self.accessable (_realpath)

    def isregular (self, path):
        # is regular file: file, dir, link
        if os.path.isfile (path) or os.path.isdir (path) or os.path.islink (path):
            return True

        return False

if '__main__' == __name__:
    print ('aha')
