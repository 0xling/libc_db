#!/usr/bin/python
#encoding:utf-8
import re
from urlparse import urljoin

__author__ = 'ling'

from common import *

def get_all_arch():
    baseurl = 'http://seblu.net/a/archive/packages/g/glibc/'
    content = curl(baseurl)
    #print content

    have_libc_files = get_all_pkg_files()
    matches = re.findall('<a href="(glibc-.*tar.xz)">', content)
    for match in matches:
        archurl = urljoin(baseurl, match)
        archfile = 'arch-'+match

        if archfile in have_libc_files:
            continue
        if get_one_arch(archurl, archfile):
            have_libc_files.append(archfile)


if __name__ == '__main__':
    get_all_arch()
