#!/usr/bin/python
# -*- coding: utf-8 -*-

import commands
import re
import sys
import os
import subprocess

os.environ['LANG']='C'

WORKDIR='./debuginfo_rpms'
REQUIREDRPMS='required_rpms.txt'
DNF='/usr/bin/dnf'
DEBUGINFO_INSTALL='/usr/bin/debuginfo-install'
flag_debug = True


def my_name():
    index = sys.argv[0].rindex('/');
    return sys.argv[0][index+1:]


THIS = my_name()


def usage():
    sys.exit('Just run ' + THIS)


def debug(message):
    if flag_debug:
        print('debug: ' + message)


def warn(message):
    print('warn: ' + message)


def has_dnf():
    return os.access(DNF, os.X_OK)


def has_debuginfo_install():
    return os.access(DEBUGINFO_INSTALL, os.X_OK)


def make_directory():
    if not os.path.exists(WORKDIR):
        os.makedirs(WORKDIR)


def get_required_package_list():
    """
    """
    with open(REQUIREDRPMS) as f:
        packages = map(lambda s: s.rstrip(), f.readlines())
    return packages


def get_debuginfo_install_command():
    """
    debuginfo-install -y --downloadonly --downloaddir=./debuginfo_rpms pkg pkg ...
    """
    command = 'debuginfo-install -y'
    command += ' --downloadonly'
    command += ' --downloaddir=' + WORKDIR
    command += ' ' + ' '.join(get_required_package_list())
    return command


def get_dnf_download_command():
    """
    dnf debuginfo-install --downloadonly --downloaddir=debuginfo_rpms pkg1 pkg2 ...
    """
    command = 'dnf debuginfo-install -y'
    command += ' --downloadonly'
    command += ' --downloaddir=' + WORKDIR
    command += ' ' + ' '.join(get_required_package_list())
    return command


def download_debuginfo_by_dnf():
    command = get_dnf_download_command()
    print('Running ' + command)
    os.system(command)


def download_debuginfo_by_yum():
    command = get_debuginfo_install_command()
    print('Running ' + command)
    os.system(command)


def download_debuginfo():
    if (has_dnf()):
        download_debuginfo_by_dnf()
    else:
        download_debuginfo_by_yum()


def unpack_debuginfo():
    files = os.listdir(WORKDIR)
    for file in files:
        file = WORKDIR + '/' + file
        print('Unpacking ' + file)
        command = 'rpm2cpio ' + file + ' | cpio -idu'
        os.system(command)


if __name__ == '__main__':
    if ((not has_dnf()) and (not has_debuginfo_install())):
        sys.exit(THIS + ' requires debuginfo-install.\nRun yum install yum-utils\n')
    make_directory()
    download_debuginfo()
    unpack_debuginfo()
    sys.exit('\n\nDebuginfo provided.\nRun ./opencore.sh')
