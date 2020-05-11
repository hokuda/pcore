#!/bin/bash

mkdir tmp
../../../rhel8.sh < ../../../src/getdebuginfo > tmp/getdebuginfo
../../../rhel8.sh < ../../../src/pcore.main > tmp/pcore.main
cp ../../run_get_debuginfo_unittest.py tmp/
podman build -t ubi8/pcore_test .
podman run ubi8/pcore_test /run_doctest.sh
podman rmi -f ubi8/pcore_test
rm -fr tmp
