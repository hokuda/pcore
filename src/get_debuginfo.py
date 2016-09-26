#!/usr/bin/python

import commands
import re
import sys
import os

flag_debug = False


def debug(message):
    if flag_debug:
        print(message)


def parse_yum_error(output):
    """
    parse the error output from yum provides command to find repository name
    """
    m = re.search(r'^.*yum-config-manager --disable (.+)$', output, flags=re.MULTILINE)
    if m != None:
        repo = m.group(1)
        if repo != None and repo != '':
            print("The repo {0} is not alive.".format(repo))
            return repo
    m = re.search(r'^.+: Cannot retrieve repository metadata \(repomd.xml\) for repository: (.+). Please verify its path and try again$', output, flags=re.MULTILINE)
    if m != None:
        repo = m.group(1)
        if repo != None and repo != '':
            print("The repo {0} is not alive.".format(repo))
            return repo
    return None


def get_unavail_repos():
    """
    trying yum info bash, add a repo to the unavailable repo list
    if yum returns non-zero,
    and returns the list of unavailable repositories
    if yum returns 0(success).
    """
    print("detecting unavailable repos")
    unavail_repos = []
    while True:
        command = 'yum --disablerepo=\'*\' --enablerepo=\'*debug*\' '
        command += ' '.join(['--disablerepo="{0}"'.format(r) for r in unavail_repos])
        command += ' info bash'
        print(command)
        (status, output) = commands.getstatusoutput(command)
        debug(output)
        debug(status)
        if status != 0:
            repo = parse_yum_error(output)
            if repo != None and repo != '':
                unavail_repos.append(repo)
            else:
                debug(output)
                sys.exit()
        else: # if status==0
            return unavail_repos
    

def is_fc24():
    revision = os.uname()[2]
    return revision.find("fc24") >= 0


unavail_repos = get_unavail_repos()
opt_unavail_repos = ' '.join(['--disablerepo="{0}"'.format(r) for r in unavail_repos])


f = open('debugfiles.txt')
debugfiles = [d.rstrip() for d in f.readlines() if re.match(r'/usr/lib/debug/.build-id/[a-z0-9]+/[a-z0-9]+', d) != None]
totalnum = len(debugfiles)
f.close()

pkgs = []

f = open('installed_rpms.txt')
rpms = ','.join(f.readlines())
f.close()

out_pattern = re.compile(r"(.*) : Debug information")
for i,df in enumerate(debugfiles, start=1):
    print("looking up {0} ({1}/{2})".format(df, str(i), str(totalnum)))
    command = "yum --disablerepo='*' --enablerepo='*debug*' "
    command += opt_unavail_repos
    command += ' provides ' + df
    debug(command)
    out = commands.getoutput(command)
    debug(out)
    out_matches = [out_pattern.match(l) for l in out.split("\n")]
    debuginfos = [m.group(1) for m in out_matches if m != None]
    debug(debuginfos)
    for d in debuginfos:
        pkg_pattern = d.replace("-debuginfo-", ".*")
        pkg_match = re.search(pkg_pattern, rpms)
        if (pkg_match != None) and not (d in pkgs):
            pkgs.append(d)
            print("Found " + d)


for pkg in pkgs:
    if is_fc24():
        command = "dnf download --disablerepo='*' --enablerepo='*debug*'"
    else:
        command = "yumdownloader --disablerepo='*' --enablerepo='*debug*' "
    command += opt_unavail_repos
    command += ' ' + pkg
    print command
    out = commands.getoutput(command)
    debug(out)
    command = "rpm2cpio " + pkg + ".rpm | cpio -id"
    print command
    out = commands.getoutput(command)
    debug(out)


sys.exit()
