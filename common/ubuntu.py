#!/usr/bin/python
# encoding:utf-8
import re

__author__ = 'ling'

import requests
from urlparse import *

root_url = 'http://security.ubuntu.com/ubuntu/pool/main/'

libcs = ['eglibc', 'glibc']


def curl(url):
    try:
        r = requests.get(url, timeout=5)
    except Exception:
        print 'Error: %s' % (url)
        return None

    print '%s: %s' % (r.status_code, url)
    if r.ok:
        return r.content
    else:
        return None

def deb_extract(debfile):
    fobj = open(debfile)
    try:
        apt_inst.deb_extract_archive(fobj, sys.argv[2])
    finally:
        fobj.close()


def get_all_ubuntu():
    for libc in libcs:
        url = urljoin(root_url, libc[0])
        url = urljoin(url + '/', libc)
        list = curl(url)
        #print list

        if list is None:
            continue

        matchs = re.findall(r'href="(libc6(-i386|-amd64)?_[^"]*.deb)"', list)

        all_libs = []
        for match in matchs:
            print match[0]
            if match[0] not in all_libs:
                all_libs.append(match[0])
                libc_url = urljoin(url+'/', match[0])
                content = curl(libc_url)

                if content is None:
                    continue

                with open('../download/ubuntu/'+match[0], 'wb') as f:
                    f.write(content)
                    f.flush()
            break


if __name__ == '__main__':
    get_all_ubuntu()
