#!/usr/bin/python3
'''
Created on 27 Dec 2019

@author: Eilon Levin
'''

class bcolors:
    HEADER = '\033[95m'
    COLOR_INFO = '\033[37m'  #
    COLOR_PASS = '\033[92m'
    COLOR_DEBUG = '\033[94m'
    COLOR_WARNING = '\033[33m'
    COLOR_FAIL = '\033[91m'
    COLOR_END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log_header(msg):
    print(bcolors.HEADER + bcolors.BOLD + msg + bcolors.COLOR_END)


def log_warning(msg):
    print(bcolors.COLOR_WARNING + msg + bcolors.COLOR_END)


def log_info(msg):
    print(bcolors.COLOR_INFO + msg + bcolors.COLOR_END)


def log_error(msg):
    print(bcolors.COLOR_FAIL + msg + bcolors.COLOR_END)


def log_pass(msg):
    print(bcolors.COLOR_PASS + msg + bcolors.COLOR_END)

def log_debug(msg):
    print(bcolors.COLOR_DEBUG + msg + bcolors.COLOR_END)
