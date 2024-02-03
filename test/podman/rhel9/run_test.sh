#!/bin/bash

mkdir tmp
cp ../../../src/getdebuginfo tmp/
cp ../../../src/pcore.main tmp/
podman build -t ubi9/pcore_test .
podman run -it ubi9/pcore_test /run_doctest.sh
podman rmi -f ubi9/pcore_test
rm -fr tmp
