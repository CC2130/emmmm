#!/usr/bin/env python3
# encoding : utf-8
# Filename: logger.py
__author__ = 'Jia Chao'

import os
import sys
import signal
import platform
import logging
from logging.handlers import RotatingFileHandler

def log_init (logdir, name, level=logging.INFO, screen=False):
    '''
    init log settings
    send SIGHUP signal can open or close debug mode
    '''

    init_log_level = level

    def debug_handler (signum, frame):
        # open or close debug mode
        if logger.level != 10:
            formatter = get_formatter (logging.DEBUG)
            new_log_level = logging.DEBUG
        elif logger.level != init_log_level:
            formatter = get_formatter (init_log_level)
            new_log_level = init_log_level

        logger.setLevel (new_log_level)
        rh.setFormatter(formatter)
        rh.setLevel (new_log_level)
        if ch:
            ch.setFormatter(formatter)
            ch.setLevel (new_log_level)

    # enable or disable debug_mode by send signal.SIGHUB
    signal.signal (signal.SIGHUP, debug_handler)

    def get_formatter (level):
        formatline = '%(asctime)s-%(levelname)s:%(message)s'
        if logging.DEBUG == level:
            formatline = '%(asctime)s-[%(filename)s](%(funcName)s)[line:%(lineno)d]%(levelname)s:%(message)s'
        return logging.Formatter(formatline)

    formatter = get_formatter (level)
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.propagate = 0
    if not os.path.isdir (logdir):
        os.makedirs (logdir, 0o755)

    if True == screen:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    logger_path = logdir + os.sep + name+'.log'
    # Max filesize 5M, keep 3 backup logs
    rh = RotatingFileHandler(logger_path, maxBytes=5*1024*1024, backupCount=3)
    rh.setLevel(level)
    rh.setFormatter(formatter)
    logger.addHandler(rh)

