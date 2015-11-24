__author__ = 'ling'

from ubuntu import *
from debian import *
from fedora import *
from arch import *
from add import *


def get(op=None):
    print 'begin get, it may take a very long time'
    if op is None:
        get_all_ubuntu()
        get_all_debian()
        get_all_fedora()
        get_all_arch()
    elif op == 'ubuntu':
        get_all_ubuntu()
    elif op == 'debian':
        get_all_debian()
    elif op == 'fedora':
        get_all_fedora()
    elif op == 'arch':
        get_all_arch()

    add_all_libc()
