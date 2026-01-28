"""
Helper, Property and Static method tests for pyunigps.UBXMessage

Created on 6 Oct 2025

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest
from io import BytesIO
import pyunigps.unitypes_core as unt
import pyunigps.exceptions as une
from pyunigps.unitypes_core import SET, GET, VALCKSUM, CV, POLL, UNI_MSGIDS
from pyunigps import UNIReader, UNIMessage
from pyunigps.unihelpers import calc_crc, escapeall

class StaticTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)


    def tearDown(self):
        pass

    def testcrc(self):

        MSG1 = b"\xaa\x44\x5b\x00\x12\x00\x05\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x11\x22\x33\x44\x55"
        res = calc_crc(MSG1)
        # print(escapeall(res))
        self.assertEqual(res, b'\xc6\xe9\x40\x60')

        MSG2 = b"\xaa\x44\x5b\x00\x14\x00\x07\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x11\x22\x33\x44\x55\x66\x77"
        res = calc_crc(MSG2)
        # print(escapeall(res))
        self.assertEqual(res,b'\x70\x19\x8f\x95')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
