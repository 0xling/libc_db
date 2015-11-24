#!/usr/bin/python
#encoding:utf-8
import httplib
from sys import argv

__author__ = 'ling'

from get import *
from add import *
from find import *
from status import *


def usage():
    use = '''
usage:
    # get the libc from internet
    libc_db.py get [ubuntu|debian|arch|fedora]

    # add a local libc to the database
    libc_db.py add <libc_file>

    # find the maybe libc through a fun address
    libc_db.py find <fun_name> <fun_addr>

    # identify the libc_file is in the database
    libc_db.py identify <libc_file>

    # check the database status
    libc_db.py status
'''
    print ''
    print use.strip()
    print ''
    exit(0)


def main():
    if len(argv) == 1:
        usage()

    if argv[1] == 'get':
        if len(argv) == 2:
            get()
        elif argv[2] in ['ubuntu', 'fedora', 'debian', 'arch']:
            get(argv[2])
        else:
            usage()
    elif argv[1] == 'add':
        try:
            libc_file = argv[2]
            add_local_libc(libc_file)
        except:
            usage()
    elif argv[1] == 'find':
        try:
            fun_name = argv[2]
            fun_addr = argv[3]
            find(fun_name, fun_addr)
        except:
            usage()
    elif argv[1] == 'identify':
        try:
            libc_file = argv[2]
            identify(libc_file)
        except:
            usage()
    elif argv[1] == 'status':
        status()
    else:
        usage()


if __name__ == '__main__':
    cur_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(argv[0])))
    main()
    os.chdir(cur_dir)


