#!/usr/bin/python
#encoding:utf-8
import re

__author__ = 'ling'

import json
from urlparse import urljoin
from common import *

def get_all_debian(download=True):
    base_url = 'http://snapshot.debian.org/'

    pkgs = ['glibc', 'eglibc']

    white_lists = ['libc6-amd64','libc6-i386','libc6-i686','libc6-x32']

    have_libc_file = get_all_pkg_files()

    pkg_urls = []

    for pkg in pkgs:
        version_url = urljoin(base_url, 'mr/package/'+pkg+'/')

        data = curl(version_url)

        versions = [y["version"] for y in json.loads(data)['result']]
        print 'versions'
        print versions

        for version in versions:
            print 'version:'+version
            binpack_url = urljoin(base_url, "mr/package/"+pkg+'/'+version+'/binpackages')
            data = curl(binpack_url)
            if data is None:
                continue
            names = [y['name'] for y in json.loads(data)['result']]
            for name in names:
                if name in white_lists:
                    binfile_url = urljoin(base_url, "mr/binary/"+name+'/'+version+'/binfiles')
                    data = curl(binfile_url)
                    if data is None:
                        continue
                    hashes = [y['hash'] for y in json.loads(data)['result']]
                    for hash in hashes:
                        deb_url = urljoin(base_url, 'file/'+hash)

                        deb_file = 'debian-'+name+'-'+version+'.deb'

                        if deb_file not in have_libc_file:
                            if download:
                                if get_one_deb(deb_url, deb_file):
                                    have_libc_file.append(deb_file)
                            else:
                                print 'get:'+deb_url
                            pkg_urls.append(deb_url)
    return pkg_urls

def get_all_debian2(download=True):
    base_url = 'http://snapshot.debian.org/'

    pkgs = ['glibc', 'eglibc']

    pkg_urls = []

    have_libc_file = get_all_pkg_files()

    for pkg in pkgs:
        version_url = urljoin(base_url, 'mr/package/'+pkg+'/')

        data = curl(version_url)

        versions = [y["version"] for y in json.loads(data)['result']]
        print 'versions'
        print versions

        for version in versions:
            if 'powerpc' in version:
                continue
            if 'alpha' in version:
                continue
            print 'version:'+version
            binpack_url = urljoin(base_url, "mr/package/"+pkg+'/'+version+'/binpackages')
            data = curl(binpack_url)
            if data is None:
                continue
            names = [y['name'] for y in json.loads(data)['result']]

            use_names = []
            for name in names:
                if ('-src' in name)|('-dev' in name) | ('udeb' in name):
                    continue
                if ('-pic' in name)|('-xen' in name) | ('-dbg' in name):
                    continue
                if ('-doc' in name)|('-bin' in name) | ('-prof' in name):
                    continue
                if ('source' in name)|('ppc' in name) | ('-powerpc' in name):
                    continue
                if ('s390' in name)|('mips' in name) | ('loongson' in name):
                    continue
                if ('alpha' in name)|('sparc' in name)|('libc-l10n' in name):
                    continue
                if 'libc' not in name:
                    continue
                use_names.append(name)
            for name in use_names:
                binfile_url = urljoin(base_url, "mr/binary/"+name+'/'+version+'/binfiles')
                data = curl(binfile_url)
                if data is None:
                    continue
                hashes = [y['hash'] for y in json.loads(data)['result']]
                for hash in hashes:
                    deb_url = urljoin(base_url, 'file/'+hash)

                    deb_file = 'debian-'+name+'-'+version+'.deb'

                    if deb_file not in have_libc_file:
                        if download:
                            if get_one_deb(deb_url, deb_file):
                                have_libc_file.append(deb_file)
                        else:
                            print 'get:'+deb_url
                        pkg_urls.append(deb_url)
    return pkg_urls

def get_all_debian3(download=True):
    base_url = 'https://packages.debian.org/'

    versions = ['squeeze-lts',
               'squeeze',
               'wheezy',
               'jessie',
               'stretch',
               'sid',
               'experimental']
    arches = ['amd64', 'i386']

    download_pkgs = get_all_pkg_files()

    pkg_urls = []

    for version in versions:
        for arch in arches:
            libc_url = urljoin(base_url, version+'/'+arch+'/libc6/download')

            content = curl(libc_url)
            if content is None:
                continue

            matches = re.findall('<a href="(http.*deb)">', content)

            deb_url = matches[0]

            deb_file = 'debian-'+os.path.basename(deb_url)

            if deb_file not in download_pkgs:
                if download:
                    if get_one_deb(deb_url, deb_file):
                        download_pkgs.append(deb_file)
                else:
                    print 'get:'+deb_url
                pkg_urls.append(deb_url)

    return pkg_urls

if __name__ == '__main__':
    get_all_debian2()