#!/bin/bash

mkdir tmp
cp ../../../src/getdebuginfo tmp/
cp ../../../src/pcore.main tmp/
cp ../../run_get_debuginfo_unittest.py tmp/
podman build -t rhel7/pcore_test .
podman run rhel7/pcore_test /run_doctest.sh
podman run rhel7/pcore_test /run_unittest.sh
podman rmi -f rhel7/pcore_test
rm -fr tmp
