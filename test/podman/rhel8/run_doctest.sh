#!/bin/bash

cd /
echo "=================== getdebuginfo doctest ======================"
ln -s getdebuginfo test
./test
rm test
echo "=================== pcore.main doctest ======================"
ln -s pcore.main test
./test
rm test pcore.main
