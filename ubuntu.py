#!/usr/bin/python
# encoding:utf-8
__author__ = 'ling'

import re
from common import *
import os
from urlparse import urljoin


def get_all_ubuntu(download=True):
    base_url = 'http://security.ubuntu.com/ubuntu/pool/main/'
    pkg_urls = []

    libcs = ['eglibc', 'glibc']
    for libc in libcs:
        url = urljoin(base_url, libc[0])
        url = urljoin(url + '/', libc)
        lists = curl(url)

        if lists is None:
            continue

        matchs = re.findall(r'href="(libc6(-i386|-amd64)?_[^"]*.deb)"', lists)

        downloaded_pkgs = get_all_pkg_files()

        for match in matchs:
            deb_file = match[0]
            if deb_file not in downloaded_pkgs:
                libc_url = urljoin(url + '/', deb_file)
                if download:
                    if get_one_deb(libc_url):
                        downloaded_pkgs.append(deb_file)
                else:
                    print 'get:'+libc_url
                pkg_urls.append(libc_url)

    return pkg_urls


def get_cur_ubuntu(download=True):
    base_url = 'http://packages.ubuntu.com/'
    pkg_urls = []

    arches = {'i386': ['libc6'], 'amd64': ['libc6', 'libc6-i386']}

    content = curl(base_url)

    matches = re.findall('<li><a href="([^"/]*)/"', content)
    downloaded_pkg_files = get_all_pkg_files()

    for match in matches:
        for arch, pkgs in arches.items():
            for pkg in pkgs:
                pkg_url = urljoin(base_url, match + '/' + arch + '/' + pkg + '/download')
                content = curl(pkg_url)

                debs = re.findall('<a href="([^"]*.deb)"', content)
                for deb_url in debs:
                    deb_file = os.path.basename(deb_url)
                    if deb_file in downloaded_pkg_files:
                        print 'have the deb file: %s' % deb_file
                        continue
                    if download:
                        if get_one_deb(deb_url):
                            downloaded_pkg_files.append(deb_file)
                    else:
                        print 'get:'+deb_url
                    pkg_urls.append(deb_url)
    return pkg_urls

def get_all_ubuntu2(download=True):
    baseurl = 'https://launchpad.net/ubuntu/'

    series = urljoin(baseurl, '+series')
    content = curl(series)
    if content is None:
        return

    pkg_urls = []

    downloaded_pkgs = get_all_pkg_files()

    matches = re.findall('<br />Successor to\n\s*<a href="/ubuntu/(.*)">', content)

    for match in matches:
        for arch in ['i386', 'amd64']:
            arch_url = urljoin(baseurl, match+'/'+arch+'/libc6/')

            content = curl(arch_url)
            if content is None:
                continue

            matches2 = re.findall('<a href="/ubuntu/('+match+'/'+arch+'/libc6/.*ubuntu.*)">.*</a>', content)

            for match2 in matches2:
                libc_url = urljoin(baseurl, match2)
                content = curl(libc_url)
                if content is None:
                    continue

                matches3 = re.findall('href="(http.*deb)">', content)
                for match3 in matches3:
                    pkg_url = match3
                    if os.path.basename(pkg_url) in downloaded_pkgs:
                        continue
                    if download:
                        if get_one_deb(pkg_url):
                            downloaded_pkgs.append(pkg_url)
                    else:
                        print 'get:'+pkg_url
                    pkg_urls.append(pkg_url)
    return pkg_urls

def import_deb_from_local(dir):
    pkg_urls = get_all_pkg_files()
    for rt, dirs, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(rt, file)
            if not file_path.endswith('.deb'):
                continue

            file_name = os.path.basename(file_path)

            if file_name in pkg_urls:
                continue

            print 'add:'+file_name
            deb_add_to_pkg_db(file_path, file_name)

            pkg_urls.append(file_name)

if __name__ == '__main__':
    pkg_urls = get_all_ubuntu2()
    print 'url........................'
    for url in pkg_urls:
        print url