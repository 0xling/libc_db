__author__ = 'ling'
from common import *


def find(name, addr_str):
    count = 0
    address = int(addr_str, 16)

    libcs = get_all_symbols_libc()

    for libc, hash in libcs.items():
        symbol_file = libc[0:-4] + 'symbols'

        f = open('./symbols/' + symbol_file, 'rb')
        for line in f:
            fun_name = line.split(' ')[0].strip()
            if name == fun_name:
                fun_addr = int(line.split(' ')[1].strip(), 16)
                if (fun_addr & 0xfff) == (address & 0xfff):
                    print libc, hash
                    count += 1
                    continue

    print 'find %d libc' % count
