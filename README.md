pcore
=====

core-analysis-aid tool for support engineers working on RHEL/Fedora platform

## Background

To analyse a user space core, you need shared libraries linked with the core. Especially if you are a support engineer, you have to have a setup exactly same as your customer's environment gathering up libraries to analyse the customer's core on your own setup. For this purpose, most of you would have to install OS (which is a little bit older than a customer's), find and install relevant versions of relevant packages reviewing sos-report, install them, and optionally download and apply relevant debuginfo.

## What it is

pcore creates tiny helper scripts to provide cross platform analysis environment easily, gathers up an executable, its core, and all of its linked shared libraries to *fake up* the customer's environment, and packages them into single tar.bz2 file. You don't need a painful task to set up an environment any longer.

## How to build

Simply type

        $ make

Then, you get pcore.zip which includes pcore script.

## Prerequisites

* pcore is written in python.
* pcore uses gdb to find libraries linked in a core. If gdb is not found, pcore uses ldd instead. ldd can find shared libraries which is explicitly specified in program header table in ELF objects, but can not take care of dynamic loading of shared libraries like Apache httpd modules. Therefore, pcore may be unable to find all of libraries.
* requires elfutils package.

## Supported Platform

* Red Hat Enterprise Linux 6.x, 7.x
* Fedora release 19~26

## How to use

1. Send pcore.zip to your customer and ask him/her to run pcore as root and send pcore-${timestamp}.tar.bz2 to you

        # unzip pcore.zip
        # cd pcore
        # ./pcore [-options]

2. Download and untar pcore-${timestamp}.tar.bz2 on a working directory on your setup.

        # tar jxvf pcore-${timestamp}.tar.bz2

3. (optional) Run getdebuginfo script. Debuginfo files are stored in the current directory. Note that it works on only a platform same as your customer's platform.

        # cd pcore-${timestamp}
        # ./getdebuginfo

4. Run opencore.sh script. It attaches gdb on a core faking up the customer's environment. It works on Fedora 19/20, RHEL 6.x, and RHEL 5.x regardless the customer's platform.

        # ./opencore.sh

## Options

    -h, --help                        show help
    -e <execfile>, --exec=<execfile>  set exec file's path name
    -c <corefile>, --core <corefile>  set core file's path name
    -n, --no-core                     do not include a core in tar.bz2
    --httpd                           assume a core is of httpd bundled in RHEL and give a hint to pcore to gather up dynamically loaded shared libraries.
    --ews-httpd=<ews install root>    assume a core is of httpd of EWS and give a hint to pcore to gather up dynamically loaded shared libraries.

## Examples

Commonly use for httpd core:

        # ./pcore -c /path/to/core -e /usr/sbin/httpd

If you do not need a core file in pcore-${timestamp}.tar.bz2:

        # ./pcore -n -c /path/to/core -e /usr/sbin/httpd

If a core is of httpd bundled in RHEL and gdb is not installed on the customer's server, ask him/her to run:

        # ./pcore -c /path/to/core -e /usr/sbin/httpd --httpd

If a core is of httpd of EWS and gdb is not installed on the customer's server, ask him/her to run:

        # ./pcore -c /path/to/core -e /opt/jboss-ews-2.0/httpd/sbin/httpd --ews-httpd=/opt/jboss-ews-2.0

## Author

Hisanobu Okuda hisanobu.okuda@gmail.com
