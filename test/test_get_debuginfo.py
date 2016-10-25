#!/usr/bin/python -O

import unittest
import sys
import os
import re
import datetime
import time
import commands

sys.path.append('../src')

import get_debuginfo

class Test100_get_debugfile_path(unittest.TestCase):

    def test_simple(self):
        actual = get_debuginfo.get_debugfile_path('1234')
        expected = '/usr/lib/debug/.build-id/12/34'
        self.assertEqual(expected, actual)


    def test_length(self):
        path = get_debuginfo.get_debugfile_path('86fe5bc1f46b8f8aa9a7a479ff991900db93f720@0x7f71aab08248')
        actual = len(path)
        expected = 66
        self.assertEqual(expected, actual)

class Test100_get_debugfile_list(unittest.TestCase):

    def test_simple(self):
        # the first is not a valid debug file
        expected = [
            '/usr/lib/debug/.build-id//',
            '/usr/lib/debug/.build-id/fe/49b5570eef894382138aed2a692b42dca39f5a',
            '/usr/lib/debug/.build-id/09/feae522af59100e6f6f2ab80bd852a4b945957',
            '/usr/lib/debug/.build-id/1f/959bd5d9a48d4259d35b2cd2fa3f04836ea92e'
        ]
        str = '\n'.join(expected)
        debug_files = 'debugfiles.txt'
        with open(debug_files, 'w') as f:
            f.write(str)

        actual = get_debuginfo.get_debugfile_list()
        self.assertNotEqual(actual, expected)

        # the first is removed
        expected = [
            '/usr/lib/debug/.build-id/fe/49b5570eef894382138aed2a692b42dca39f5a',
            '/usr/lib/debug/.build-id/09/feae522af59100e6f6f2ab80bd852a4b945957',
            '/usr/lib/debug/.build-id/1f/959bd5d9a48d4259d35b2cd2fa3f04836ea92e'
        ]
        self.assertEqual(actual, expected)
        os.unlink(debug_files)


if __name__ == "__main__":
    unittest.main()
