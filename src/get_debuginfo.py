#!/usr/bin/python
# -*- coding: utf-8 -*-

import commands
import re
import sys
import os
import subprocess

os.environ['LANG']='C'

WORKDIR='./debuginfo_rpms'
DEBUG_FILES='debugfiles.txt'
INSTALL='install'
REINSTALL='reinstall'
DNF='/usr/bin/dnf'
YUM='/usr/bin/yum'
YUMDOWNLOADER='/usr/bin/yumdownloader'
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


def parse_yum_error(output):
    """
    parses the error output from yum provides command to find repository name
    if error is found, returns its repository name
    otherwise, returns None
    """
    m = re.search(r'^.*yum-config-manager --disable (.+)$', output, flags=re.MULTILINE)
    if m != None:
        repo = m.group(1)
        if repo != None and repo != '':
            print('The repo {0} is not alive.'.format(repo))
            return repo
    m = re.search(r'^.+: Cannot retrieve repository metadata \(repomd.xml\) for repository: (.+). Please verify its path and try again$', output, flags=re.MULTILINE)
    if m != None:
        repo = m.group(1)
        if repo != None and repo != '':
            print('The repo {0} is not alive.'.format(repo))
            return repo
    return None


"""
The latest yum in RHEL7 fails when the --disablerepo option specifies non-existing repo.
Since inserting '*' in somewhere in a repo name can avoid it, every repo name in unavail_repos must have '*'.
"""
UNAVAIL_REPOS = [
    'jws-3*', '*beta*', '*rhmap*',
    'rhel-*-server-insights-3-debug-rpms',
    'rhel-atomic-7-cdk-3.*-debug-rpms',
    'rhel-6-server-satellite-tools-6.3-puppet4-debug-rpms*',
    'rhel-6-server-*-satellite-tools-6.3-puppet4-debug-rpms',
    'rhel-7-server-satellite-tools-6.3-puppet4-debug-rpms*',
    'rhel-7-server-*-satellite-tools-6.3-puppet4-debug-rpms',
    'rhel-7-server-ansible-2-debug-rpms*',
    'rhel-7-server-ansible-2.5-debug-rpms*'
]


def get_unavail_repos():
    """
    ping repositories trying `yum/dnf info bash` and returns an unavailable repo list
    """
    print('detecting unavailable repos...')
    unavail_repos = list(UNAVAIL_REPOS)
    while True:
        command = 'yum -y --disablerepo=* --enablerepo=*debug* '
        command += ' '.join(['--disablerepo={0}'.format(r) for r in unavail_repos])
        command += ' info bash'
        debug(command)
        (status, output) = commands.getstatusoutput(command)
        # hokuda uncomment
        #(status, output) = (0, None)
        debug('output=' + output)
        debug('status=' + str(status))
        if status != 0:
            repo = parse_yum_error(output)
            if repo != None and repo != '':
                unavail_repos.append(repo)
            else:
                print('failed to find an unavailable repository')
                debug(output)
                sys.exit()
        else: # if status==0
            return unavail_repos
    

def is_fc24():
    revision = os.uname()[2]
    return revision.find('fc24') >= 0


def has_dnf():
    return os.access(DNF, os.X_OK)


def has_yumdownloader():
    return os.access(YUMDOWNLOADER, os.X_OK)


def make_directory():
    if not os.path.exists(WORKDIR):
        os.makedirs(WORKDIR)


def get_debugfile_path(build_id):
    """
    convert build id to debug file path, i.e,
    get_debugfile_path('86fe5bc1f46b8f8aa9a7a479ff991900db93f720@0x7f71aab08248') == '/usr/lib/debug/.build-id/86/fe5bc1f46b8f8aa9a7a479ff991900db93f720'
    """
    if len(build_id.split('@')[0]) != 40:
        warn('build id must be 40 bytes length')
    return '/usr/lib/debug/.build-id/' + build_id[0:2] + '/' + build_id[2:40]


def get_debugfile_list():
    """
    """
    with open(DEBUG_FILES) as f:
        debugfiles = [line.rstrip() for line in f.readlines()
                      if re.match(r'/usr/lib/debug/.build-id/[a-z0-9]+/[a-z0-9]+', line) != None]
    return debugfiles


def get_debugfile_list_eu_unstrip(path_to_core):
    """
    get build-id invoking eu-unstrip -n --core=coredump
    TODO: it does not work. why?
    """
    command = "eu-unstrip -n --core=" + path_to_core
    out = commands.getoutput(command)
    lines = out.split('\n')
    ids = map(lambda x: x.split()[1], lines)
    list = map(get_debugfile_path, ids)
    return list


def get_yum_install_command(unavail_repos):
    """
    yum <subcommand> -y --enablerepo "*debug*" --downloadonly --downloaddir=. /usr/lib/debug/.build-id/ff/246dbc378d5afc4885c6bc26d3190b76321a35
    """
    # For unknown reason, the "install" sub command does not work, when an
    # argument to the --enablerepo/disablerepo option only for quoted by
    # ' and ", like "--disablerepo=\'*\'".
    opt_unavail_repos = ' '.join(['--disablerepo={0}'.format(r) for r in unavail_repos])
    command = 'yum install'
    command += ' --assumeno --disablerepo=* --enablerepo=*debug* --downloadonly --downloaddir=.'
    command += ' ' + opt_unavail_repos
    command += ' ' + ' '.join(get_debugfile_list())
    return command


def get_yumdownloader_command(unavail_repos, packages):
    """
    yumdownloader --enablerepo "*debug*" pkg pkg ...
    """
    opt_unavail_repos = ' '.join(['--disablerepo={0}'.format(r) for r in unavail_repos])
    command = 'yumdownloader'
    command += ' --disablerepo=* --enablerepo=*debug*'
    command += ' ' + opt_unavail_repos
    command += ' ' + ' '.join(packages)
    debug(command)
    return command


def get_dnf_download_command(unavail_repos, rpms):
    """
    dnf download --disablerepo='*' --enablerepo='*debug*' --destdir=xxx /usr/lib/debug/.build-id/ff/246dbc378d5afc4885c6bc26d3190b76321a35
    """
    opt_unavail_repos = ' '.join(['--disablerepo="{0}"'.format(r) for r in unavail_repos])
    command = 'dnf download --disablerepo="*" --enablerepo="*debug*"'
    command += ' ' + opt_unavail_repos
    command += ' ' + ' '.join(rpms)
    return command


def get_dnf_provides_command(unavail_repos):
    """
    dnf provides -q --disablerepo='*' --enablerepo='*debug*' --destdir=xxx /usr/lib/debug/.build-id/ff/246dbc378d5afc4885c6bc26d3190b76321a35 ...
    """
    opt_unavail_repos = ' '.join(['--disablerepo="{0}"'.format(r) for r in unavail_repos])
    command = DNF + ' provides -q --disablerepo="*" --enablerepo="*debug*"'
    command += ' ' + opt_unavail_repos
    command += ' ' + ' '.join(get_debugfile_list())
    return command


def parse_dnf_provides_output(out):
    """
    parse `dnf provies` output to get debuginfo package names

    >>> out = \"\"\"httpd-debuginfo-2.4.33-5.fc27.x86_64 : Debug information for package httpd
    ... Repo        : updates-debuginfo
    ... Matched from: 
    ... Filename    : /usr/lib/debug/.build-id/a8/b5bae4f6277ac65272adbff8f8492104211a72
    ... Filename    : /usr/lib/debug/.build-id/61/8cf77df1ea3a34d773d0c0b5fb2aea5641cf70
    ... Filename    : /usr/lib/debug/.build-id/c0/c8973b70af790394a36c8999b566be99152a8a
    ... 
    ... avahi-libs-debuginfo-0.7-11.fc27.x86_64 : Debug information for package avahi-libs
    ... Repo        : updates-debuginfo
    ... Matched from: 
    ... Filename    : /usr/lib/debug/.build-id/ec/4c993eb606fedada13b0d4ddbb5b743b552577
    ... \"\"\"
    >>> rpms = parse_dnf_provides_output(out)
    debug: parse_dnf_provides_output: Found httpd-debuginfo-2.4.33-5.fc27.x86_64
    debug: parse_dnf_provides_output: Found avahi-libs-debuginfo-0.7-11.fc27.x86_64
    """
    rpms = []
    rpm = None
    for l in out.split('\n'):
        if rpm == None:
            rpm = l.split(' : ')[0]
            rpms.append(rpm)
            debug("parse_dnf_provides_output: Found " + rpm)
        elif l == "":
            rpm = None
    return list(set(rpms))


def download_debuginfo_by_dnf():
    unavail_repos = get_unavail_repos()

    # get debuginfo package names
    command = get_dnf_provides_command(unavail_repos)
    print('Running ' + command)
    out = commands.getoutput(command)
    debug("download_debuginfo_by_dnf: out=" + out)
    rpms = parse_dnf_provides_output(out)

    command = get_dnf_download_command(unavail_repos, rpms)
    print('Running ' + command)
    os.chdir(WORKDIR)
    os.system(command)
    os.chdir('..')

# ---> Package bash-debuginfo.x86_64 0:4.2.46-19.el7 will be installed
PATTERN0 = re.compile(r'---> Package (.+)\.(.+) 0:(.+) will be installed')

# Package matching e2fsprogs-debuginfo-1.42.9-7.el7.x86_64 already installed. Checking for update.
PATTERN1 = re.compile(r'Package matching (.+) already installed. Checking for update.')

# Package elfutils-debuginfo-0.163-3.el7.x86_64 already installed and latest version
PATTERN2 = re.compile(r'Package (.+) already installed and latest version')

def parse_line_to_find_installed_package(line):
    match = PATTERN0.match(line)
    if (match):
        debug('parse_line_to_find_installed_package: parsed(0) ' + line)
        return match.group(1) + '-' + match.group(3) + '.' + match.group(2)
    match = PATTERN1.match(line)
    if (match):
        debug('parse_line_to_find_installed_package: parsed(1) ' + line)
        return match.group(1)
    match = PATTERN2.match(line)
    if (match):
        debug('parse_line_to_find_installed_package: parsed(2) ' + line)
        return match.group(1)
    return None


def parse_yum_install_output(out):
    packages = []
    for line in out.split('\n'):
        package = parse_line_to_find_installed_package(line)
        if package:
            packages.append(package)
    return packages


def download_debuginfo_by_yum():
    unavail_repos = get_unavail_repos()

    # search for necessary debuginfo packages
    command = get_yum_install_command(unavail_repos)
    print('Running ' + command)
    proc = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
    out, err = proc.communicate()
    packages = parse_yum_install_output(out)
    debug(str(packages))
    
    os.chdir(WORKDIR)
    command = get_yumdownloader_command(unavail_repos, packages)
    os.system(command)
    os.chdir('..')


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
    if __file__ == "./test":
        import doctest
        doctest.testmod(verbose=True)
        sys.exit(0)
    if ((not has_dnf()) and (not has_yumdownloader())):
        sys.exit(THIS + ' requires yumdownloader.\nRun yum install yum-utils\n')
    make_directory()
    download_debuginfo()
    unpack_debuginfo()
    sys.exit('\n\nDebuginfo provided.\nRun ./opencore.sh')
