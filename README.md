pcore
=====

core-analysis-aid tool for support engineers analyzing RHEL coredump file on Fedora platform

## Background

To analyse a user space core, you need shared libraries linked with the core. Especially if you are a support engineer, you have to have a setup exactly same as your customer's environment gathering up libraries to analyse the customer's core on your own setup. For this purpose, most of you would have to install OS (which is a little bit older than a customer's), find and install relevant versions of relevant packages reviewing sos-report, install them, and optionally download and apply relevant debuginfo.

## What it is

pcore creates tiny helper scripts to provide cross platform analysis environment easily, gathers up an executable, its core, and all of its linked shared libraries to *fake up* the customer's environment, and packages them into single tar.bz2 file. You don't need a painful task to set up an environment any longer.

## How to build

        $ make

Then, you get pcore.rhel8.zip which includes pcore script.

## Prerequisites

* pcore is written in python.
* requires elfutils package.

## Tested Debugee Platform

* Red Hat Enterprise Linux 8.x

## Tested Debugger Platform

* Fedora release 35

## How to use

1. Send pcore.zip (or pcore.rhel8.zip if RHEL8) to your customer and ask him/her to run pcore as root and send pcore-${timestamp}.tar.bz2 to you

        # unzip pcore(.rhel8).zip
        # cd pcore(.rhel8)
        # ./pcore [-options]

2. Download and untar pcore-${timestamp}.tar.bz2 on a working directory on your setup.

        # tar jxvf pcore-${timestamp}.tar.bz2

3. (optional) Run getdebuginfo script. Debuginfo files are stored in the current directory. Note that it works on only a platform same as your customer's platform (RHEL7 or 8).

        # cd pcore-${timestamp}
        # ./getdebuginfo

4. Run opencore.sh script. It attaches gdb on a core faking up the customer's environment. It works on Fedora 29-30 regardless the customer's platform.

        # ./opencore.sh

## Options

    -h, --help                        show help
    -e <execfile>, --exec <execfile>  set exec file's path name
    -c <corefile>, --core <corefile>  set core file's path name
    -n, --no-core                     do not include a core in tar.bz2

## Examples

Commonly use for httpd core:

        # ./pcore -c /path/to/core -e /usr/sbin/httpd

If you do not need a core file in pcore-${timestamp}.tar.bz2:

        # ./pcore -n -c /path/to/core -e /usr/sbin/httpd

## Author

Hisanobu Okuda hisanobu.okuda@gmail.com
