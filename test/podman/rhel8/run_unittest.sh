#!/bin/bash

cd /
echo '======================== getdebuginfo unittest =========================='
cp getdebuginfo getdebuginfo.py
/usr/libexec/platform-python /run_get_debuginfo_unittest.py
