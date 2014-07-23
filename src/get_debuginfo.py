#!/usr/bin/python

import commands
import re
import sys

f = open('debugfiles.txt')
debugfiles = f.readlines()
totalnum = len(debugfiles)
f.close()

pkgs = []

f = open('installed_rpms.txt')
rpms = ','.join(f.readlines())
f.close()

out_pattern = re.compile(r"(.*) : Debug information")
i = 0
for df in debugfiles:
    i = i + 1
    df = df.rstrip()
    print "looking up " + df + " (" + str(i) + "/" + str(totalnum) + ")\n"
    #command = "yum --disablerepo='*' --enablerepo='*debug*' provides " + df + " |awk '/(.*) : Debug information.*/{print $1}'"
    command = "yum --disablerepo='*' --enablerepo='*debug*' provides " + df
    print command
    out = commands.getoutput(command)
    print out
    out_matches = [out_pattern.match(l) for l in out.split("\n")]
    debuginfos = [m.group(1) for m in out_matches if m != None]
    print debuginfos
    for d in debuginfos:
        pkg_pattern = d.replace("-debuginfo-", ".*")
        pkg_match = re.search(pkg_pattern, rpms)
        if (pkg_match != None) and not (d in pkgs):
            pkgs.append(d)
        
    #pkg = commands.getoutput(command)
    #print pkg
    #if pkg not in pkgs:
    #    pkgs.append(pkg)

print "pkg="
print pkgs

for pkg in pkgs:
    command = "yumdownloader --disablerepo='*' --enablerepo='*debug*' " + pkg
    print command
    out = commands.getoutput(command)
    print out
    command = "rpm2cpio " + pkg + ".rpm | cpio -id"
    print command
    out = commands.getoutput(command)
    print out


sys.exit()
