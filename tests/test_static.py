"""
Helper, Property and Static method tests for pyunigps.UNIMessage

Created on 26 Jan 2026

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest
import pyunigps.unitypes_core as unt
import pyunigps.exceptions as une
from pyunigps.unitypes_core import CV, UNI_MSGIDS
from pyunigps.unihelpers import (
    calc_crc,
    escapeall,
    att2idx,
    att2name,
    attsiz,
    get_bits,
    val2bytes,
    bytes2val,
    nomval,
    key_from_val,
)


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
        self.assertEqual(res, b"\xc6\xe9\x40\x60")

        MSG2 = b"\xaa\x44\x5b\x00\x14\x00\x07\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x11\x22\x33\x44\x55\x66\x77"
        res = calc_crc(MSG2)
        # print(escapeall(res))
        self.assertEqual(res, b"\x70\x19\x8f\x95")

    def testVal2Bytes(self):  # test conversion of value to bytes
        INPUTS = [
            (2345, unt.U2),
            (b"\x44\x55", unt.X2),
            (23.12345678, unt.R4),
            (-23.12345678912345, unt.R8),
            ("test1234", unt.C8),
        ]
        EXPECTED_RESULTS = [
            b"\x29\x09",
            b"\x44\x55",
            b"\xd7\xfc\xb8\x41",
            b"\x1f\xc1\x37\xdd\x9a\x1f\x37\xc0",
            "test1234",
        ]
        for i, inp in enumerate(INPUTS):
            val, att = inp
            res = val2bytes(val, att)
            self.assertEqual(res, EXPECTED_RESULTS[i])

    def testVal2BytesInvalid(self):
        with self.assertRaisesRegex(une.UNITypeError, "Unknown attribute type Y002"):
            res = val2bytes(1234, "Y002")

    def testBytes2Val(self):  # test conversion of bytes to value
        INPUTS = [
            (b"\x29\x09", unt.U2),
            (b"\x44\x55", unt.X2),
            (b"\xd7\xfc\xb8\x41", unt.R4),
            (b"\x1f\xc1\x37\xdd\x9a\x1f\x37\xc0", unt.R8),
            (b"test1234", unt.C8),
        ]
        EXPECTED_RESULTS = [
            2345,
            b"\x44\x55",
            23.12345678,
            -23.12345678912345,
            "test1234",
        ]
        for i, inp in enumerate(INPUTS):
            valb, att = inp
            res = bytes2val(valb, att)
            if att == unt.R4:
                self.assertAlmostEqual(res, EXPECTED_RESULTS[i], 6)
            elif att == unt.R8:
                self.assertAlmostEqual(res, EXPECTED_RESULTS[i], 14)
            else:
                self.assertEqual(res, EXPECTED_RESULTS[i])

    def testBytes2ValInvalid(self):
        with self.assertRaisesRegex(une.UNITypeError, "Unknown attribute type Y002"):
            res = bytes2val(b"\x12\x34", "Y002")

    def testNomval(self):  # test conversion of value to bytes
        INPUTS = [
            unt.U2,
            unt.X2,
            unt.R4,
            unt.R8,
            unt.C8,
        ]
        EXPECTED_RESULTS = [
            0,
            b"\x00\x00",
            0.0,
            0.0,
            "        ",
        ]
        for i, att in enumerate(INPUTS):
            res = nomval(att)
            self.assertEqual(res, EXPECTED_RESULTS[i])

    def testNomValInvalid(self):
        with self.assertRaisesRegex(une.UNITypeError, "Unknown attribute type Y002"):
            res = nomval("Y002")

    def testgetbits(self):
        INPUTS = [
            (b"\x89", 192),
            (b"\xc9", 3),
            (b"\x89", 9),
            (b"\xc9", 9),
            (b"\x18\x18", 8),
            (b"\x18\x20", 8),
        ]
        EXPECTED_RESULTS = [2, 1, 9, 9, 1, 0]
        for i, (vb, mask) in enumerate(INPUTS):
            vi = get_bits(vb, mask)
            self.assertEqual(vi, EXPECTED_RESULTS[i])

    def testattsiz(self):  # test attsiz
        self.assertEqual(attsiz(CV), -1)
        self.assertEqual(attsiz("C032"), 32)

    def testatt2idx(self):  # test att2idx
        EXPECTED_RESULT = [4, 16, 101, 0, (3, 6), 0]
        atts = ["svid_04", "gnssId_16", "cno_101", "gmsLon", "gnod_03_06", "dodgy_xx"]
        for i, att in enumerate(atts):
            res = att2idx(att)
            # print(res)
            self.assertEqual(res, EXPECTED_RESULT[i])

    def testatt2name(self):  # test att2name
        EXPECTED_RESULT = ["svid", "gnssId", "cno", "gmsLon"]
        atts = ["svid_04", "gnssId_16", "cno_101", "gmsLon"]
        for i, att in enumerate(atts):
            res = att2name(att)
            # print(res)
            self.assertEqual(res, EXPECTED_RESULT[i])

    def testescapeall(self):
        EXPECTED_RESULT = "b'\\x68\\x65\\x72\\x65\\x61\\x72\\x65\\x73\\x6f\\x6d\\x65\\x63\\x68\\x61\\x72\\x73'"
        val = b"herearesomechars"
        res = escapeall(val)
        print(res)
        self.assertEqual(res, EXPECTED_RESULT)

    def testkeyfromval(self):
        res = key_from_val(UNI_MSGIDS, "GLOEPH")
        self.assertEqual(res, 107)

    def testkeyfromvalinvalid(self):
        with self.assertRaisesRegex(KeyError, "No key found for value XXXX"):
            res = key_from_val(UNI_MSGIDS, "XXXX")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
