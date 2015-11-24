#!/usr/bin/python
# encoding:utf-8
__author__ = 'ling'

import os
import requests
import shutil
import struct
from config import *

def get_status_code(url):
    code = requests.get(url).status_code
    return code


def curl(url):
    try:
        print 'curl: %s' % url
        r = requests.get(url)
    except:
        print 'Error: %s' % url
        return None

    print '%s: %s' % (r.status_code, url)
    if r.ok:
        return r.content
    else:
        return None


def find_file(filename):
    for rt, dirs, files in os.walk('.'):
        for file in files:
            if file == filename:
                return os.path.join(rt, file)
    return None


def find_files(filename):
    results = []
    find = False
    for rt, dirs, files in os.walk('.'):
        for file in files:
            if file == filename:
                find = True
                results.append(os.path.join(rt, file))
    if find:
        return results
    else:
        return None


def deb_extract(deb_path):
    cur_dir = os.getcwd()
    shutil.copy(deb_path, deb_tmp_dir)

    os.chdir(deb_tmp_dir)

    deb_file = os.path.basename(deb_path)

    cmd = 'ar x ' + deb_file
    os.popen(cmd)
    try:
        cmd2 = 'tar xf data.tar.*'
        os.popen(cmd2)
    except:
        pass
    libc = find_file('libc.so.6')

    remove_cmd = 'rm -rf .'+deb_tmp_dir+'*'

    if libc is None:
        os.chdir(cur_dir)
        os.popen(remove_cmd)
        return None
    libc = os.path.realpath(libc)

    new_libc = './libc/' + deb_file[0:-4] + '.so.6'
    os.chdir(cur_dir)

    shutil.copy(libc, new_libc)
    os.popen(remove_cmd)
    return new_libc


def arch_extract(arch_path):
    cur_dir = os.getcwd()
    shutil.copy(arch_path, arch_tmp_dir)

    arch_file = os.path.basename(arch_path)

    os.chdir(arch_tmp_dir)

    cmd = 'xz -d ' + arch_file
    os.popen(cmd)
    cmd2 = 'tar -xvf ' + arch_file[0:-3] + ' 1>/dev/null 2>&1'
    os.popen(cmd2)
    libc = find_file('libc.so.6')

    remove_cmd = 'rm -rf '+arch_tmp_dir+'*'
    if libc is None:
        os.chdir(cur_dir)
        os.popen(remove_cmd)
        return None
    libc = os.path.realpath(libc)

    new_libc = './libc/' + arch_file[0:-11] + '.so.6'
    os.chdir(cur_dir)
    shutil.copy(libc, new_libc)
    os.popen(remove_cmd)
    return new_libc


def rpm_extract(rpm_path):
    cur_dir = os.getcwd()
    shutil.copy(rpm_path, rpm_tmp_dir)

    os.chdir(rpm_tmp_dir)
    rpm_file = os.path.basename(rpm_path)

    cmd = 'rpm2cpio ' + rpm_file + ' | cpio -div > /dev/null 2>/dev/null'
    os.popen(cmd)

    libcs = find_files('libc.so.6')
    remove_cmd = 'rm -rf '+rpm_tmp_dir+'*'

    if libcs is None:
        os.chdir(cur_dir)
        os.popen(remove_cmd)
        return None

    for libc in libcs:
        libc = os.path.realpath(libc)
        if 'nosegneg' in libc:
            new_libc = './libc/' + rpm_file[0:-4] + '-nosegneg.so.6'
        else:
            new_libc = './libc/' + rpm_file[0:-4] + '.so.6'
        os.chdir(cur_dir)
        shutil.copy(libc, new_libc)
        os.popen(remove_cmd)
        return new_libc


def get_all_pkg_files():
    have_deb_files = []
    f = open(pkg_db_file, 'rb')
    for line in f:
        if not line.startswith('#'):
            have_deb_files.append(line.split(' ')[1].strip('\n'))
    f.close()
    return have_deb_files


def get_all_symbols_libc():
    symbols = {}
    f = open(symbol_db_file, 'rb')
    for line in f:
        if not line.startswith('#'):
            hash = line.split(' ')[0].strip('\n')
            name = line.split(' ')[1].strip('\n')
            symbols[name] = hash
    f.close()
    return symbols

def get_sha1(file):
    hash = os.popen('sha1sum ' + file).read().split(' ')[0]
    if len(hash) != 40:
        print 'get hash fail:' + file
        return None
    return hash

def arch_add_to_pkg_db(arch_path):
    new_libc = arch_extract(arch_path)
    arch_file = os.path.basename(arch_path)

    if new_libc is None:
        print 'not find libc.so.6:' + arch_file
        return False

    hash = get_sha1(new_libc)
    if hash is None:
        return False

    with open(pkg_db_file, 'ab+') as f:
        f.write(hash + ' ' + arch_file + '\n')
        f.flush()

    return True

def get_one_arch(arch_url, arch_file):
    if arch_file is None:
        arch_file = os.path.basename(arch_url)

    print 'get_one_arch:%s, %s' % (arch_file, arch_url)

    data = curl(arch_url)
    if data is None:
        return False

    with open(arch_save_dir + arch_file, 'wb') as f:
        f.write(data)
        f.flush()

    return arch_add_to_pkg_db(arch_save_dir + arch_file)

def deb_add_to_pkg_db(deb_path):
    new_libc = deb_extract(deb_path)

    deb_file = os.path.basename(deb_path)
    if new_libc is None:
        print 'not find libc.so.6:' + deb_file
        return False

    hash = get_sha1(new_libc)
    if hash is None:
        return False

    with open(pkg_db_file, 'ab+') as f:
        f.write(hash + ' ' + deb_file + '\n')
        f.flush()

    return True


# 下载成功返回True,否则返回false
def get_one_deb(deb_url, deb_file=None):
    if deb_file is None:
        deb_file = os.path.basename(deb_url)

    print 'get_one_deb:%s, %s' % (deb_file, deb_url)
    content = curl(deb_url)

    if content is None:
        return False

    with open(deb_save_dir + deb_file, 'wb') as f:
        f.write(content)
        f.flush()

    return deb_add_to_pkg_db(deb_save_dir + deb_file)

def rpm_add_to_pkg_db(rpm_path):
    new_libc = rpm_extract(rpm_path)

    rpm_file = os.path.basename(new_libc)
    if new_libc is None:
        print 'not find libc.so.6:' + rpm_file
        return False

    hash = get_sha1(file)
    if hash is None:
        return False

    with open(pkg_db_file, 'ab+') as f:
        f.write(hash + ' ' + rpm_file + '\n')
        f.flush()

    return True

def get_one_rpm(rpm_url, rpm_file=None):
    if rpm_file is None:
        rpm_file = os.path.basename(rpm_url)

    print 'get_one_rpm:%s %s' % (rpm_file, rpm_url)

    content = curl(rpm_url)

    if content is None:
        return False

    with open(rpm_save_dir + rpm_file, 'wb') as f:
        f.write(content)
        f.flush()

    return rpm_add_to_pkg_db(rpm_save_dir + rpm_file)


# only support i386 and x86_64
def check_arch(libc_file):
    try:
        with open(libc_file, 'rb') as f:
            d = f.read(0x20)

        machine = struct.unpack("<H", d[0x12:0x14])[0]

        # 3 i386
        # 0x3e x86_64
        if (machine == 3) | (machine == 0x3e):
            return True
    except:
        pass
    return False
