#!/usr/bin/python
#encoding:utf-8
import re

__author__ = 'ling'

from common import *
from urlparse import urljoin

def get_all_update_fedora(download=True):
    downloaded_pkgs = get_all_pkg_files()
    pkg_urls = []
    for version in range(7, 24):
        if version <= 20:
            base_url = 'https://dl.fedoraproject.org/pub/archive/fedora/linux/updates/'
        else:
            base_url = 'https://archives.fedoraproject.org/pub/fedora/linux/updates/'
        if (version == 8) | (version == 9):
            pkg_url = urljoin(base_url, str(version)+'/x86_64.newkey/')
        else:
            pkg_url = urljoin(base_url, str(version)+'/x86_64/')
        content = curl(pkg_url)
        if content is None:
            continue

        matches = re.findall('<a href="(glibc-\d[^"]*.rpm)"', content)
        print matches

        for match in matches:
            rpm_file = match
            rpm_url = urljoin(pkg_url, rpm_file)

            rpm_file = 'fedora-'+rpm_file
            if rpm_file in downloaded_pkgs:
                continue
            if download:
                if get_one_rpm(rpm_url, rpm_file):
                    downloaded_pkgs.append(rpm_file)
            else:
                print 'get:'+rpm_url
            pkg_urls.append(rpm_url)

    return pkg_urls

def get_all_release_fedora(download=True):
    downloaded_pkgs = get_all_pkg_files()
    for version in range(7, 24):
        if version <= 20:
            base_url = 'https://dl.fedoraproject.org/pub/archive/fedora/linux/releases/'
        else:
            base_url = 'https://archives.fedoraproject.org/pub/fedora/linux/releases/'
        if version == 7:
            pkg_urls = [urljoin(base_url, str(version)+'/Everything/x86_64/os/Fedora/')]
        elif version <= 16:
            pkg_urls = [urljoin(base_url, str(version)+'/Everything/x86_64/os/Packages/')]
        else:
            pkg_urls = [urljoin(base_url, str(version)+'/Everything/x86_64/os/Packages/g/')]

        for pkg_url in pkg_urls:
            content = curl(pkg_url)
            if content is None:
                continue

            matches = re.findall('<a href="(glibc-\d[^"]*.rpm)"', content)
            print matches

            for match in matches:
                rpm_file = match
                rpm_url = urljoin(pkg_url, rpm_file)

                rpm_file = 'fedora-'+rpm_file
                if rpm_file in downloaded_pkgs:
                    continue
                if download:
                    if get_one_rpm(rpm_url, rpm_file):
                        downloaded_pkgs.append(rpm_file)
                else:
                    print 'get:'+rpm_url
                pkg_urls.append(rpm_url)
    return pkg_urls

def get_all_fedora():
    get_all_update_fedora()
    get_all_release_fedora()

if __name__ == '__main__':
    get_all_fedora()
