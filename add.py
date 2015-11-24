#!/usr/bin/python
#encoding:utf-8
__author__ = 'ling'

from ELFfile import *
from capstone import *
from common import *
from identify import *

def add_one_libc(libc_file, filename=None):
    print 'add_one_libc:'+libc_file
    elf = Elf(libc_file)
    if filename is None:
        filename = os.path.basename(libc_file)

    symbol_name = './symbols/'+filename[0:-4]+'symbols'

    f = open(symbol_name, 'wb')
    for name, value in elf.symbol.items():
        f.write(name+' '+hex(value)[2:].strip('Ll')+'\n')

    addr = elf.find_str('/bin/sh')
    f.write('str_bin_sh '+hex(addr)[2:].strip('Ll')+'\n')

    if elf.bits == 32:
        md = Cs(CS_ARCH_X86, CS_MODE_32)
    else:
        md = Cs(CS_ARCH_X86, CS_MODE_64)

    # __libc_start_main_ret
    # find the last call before call exit
    addr = elf.symbol['__libc_start_main']
    exit_addr = elf.symbol['exit']

    offset = elf.vma2offset(addr)

    code = elf.data[offset:offset+0x200]

    last_addr = 0
    for (address, size, mnemonic, op_str) in md.disasm_lite(code, addr):
        if mnemonic == 'call':
            try:
                call_target = int(op_str, 16)
                if call_target == exit_addr:
                    break
            except:
                pass
            last_addr = address
    f.write('__libc_start_main_ret '+hex(last_addr)[2:].strip('Ll')+'\n')
    f.close()

    f2 = open(symbol_db_file, 'ab')
    hash = get_sha1(libc_file)
    f2.write(hash+' '+os.path.basename(libc_file)+'\n')
    f2.close()

def add_all_libc():
    f = open(pkg_db_file, 'rb')

    symbol_libcs = get_all_symbols_libc()
    for line in f:
        if not line.startswith('#'):
            hash = line.split(' ')[0].strip('\n')
            name = line.split(' ')[1].strip('\n')
            if name.endswith('.deb'):
                libc_name = name[0:-4]+'.so.6'
            elif name.endswith('.rpm'):
                libc_name = name[0:-4]+'.so.6'
            elif name.endswith('.pkg.tar.xz'):
                libc_name = name[0:-11]+'.so.6'

            if symbol_libcs.has_key(libc_name):
                continue

            if not check_arch('./libc/'+libc_name):
                print 'not known arch libc:'+libc_name
                continue

            add_one_libc('./libc/'+libc_name)
            symbol_libcs[libc_name] = hash

    f.close()

def get_unique_name(libc_file):
    libc_dict = get_all_symbols_libc()
    for i in range(1000):
        name = 'local-'+str(i)+'-'+os.path.basename(libc_file)
        if libc_dict.has_key(name):
            continue
        return name

    # this is impossible
    print 'get_unique_name fail\n'
    return None

def add_local_libc(libc_file):
    count = real_identify(libc_file)
    if count == 0:
        if not libc_file.endswith('.so.6'):
            libc_file += '.so.6'
        name = get_unique_name(libc_file)
        add_one_libc(libc_file, name)
    else:
        print 'libc_file has already existed'

if __name__ == '__main__':
    add_all_libc()

