#!/usr/bin/python
# encoding:utf-8
__author__ = 'ling'

from common import *


def real_identify(libc_file):
    count = 0
    libc_hash = get_sha1(libc_file)
    if libc_hash is None:
        return

    f = open(symbol_db_file, 'rb')
    for line in f:
        hash = line.split(' ')[0].strip()
        name = line.split(' ')[1].strip()

        if hash == libc_hash:
            print name, hash
            count += 1
    f.close()

    return count


def identify(libc_file):
    count = real_identify(libc_file)
    print 'identify %d libc_file' % count
