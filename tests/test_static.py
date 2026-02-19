"""
Helper, Property and Static method tests for pyunigps.UNIMessage

Created on 26 Jan 2026

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import unittest
from datetime import datetime, timezone

import pyunigps.exceptions as une
import pyunigps.unitypes_core as unt
from pyunigps.unihelpers import (
    attsiz,
    bytes2val,
    calc_crc,
    escapeall,
    header2bytes,
    header2vals,
    msgname2id,
    nomval,
    utc2wnotow,
    val2bytes,
)
from pyunigps.unitypes_core import CV, UNI_MSGIDS


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

    def testmsgname2id(self):
        self.assertEqual(msgname2id("VERSION"), 37)
        self.assertEqual(msgname2id("version"), 37)
        self.assertEqual(msgname2id("PPPNAV"), 1026)
        self.assertEqual(msgname2id("XXXXX"), None)

    def testVal2Bytes(self):  # test conversion of value to bytes
        INPUTS = [
            (2345, unt.U2),
            (b"\x44\x55", unt.X2),
            (23.12345678, unt.R4),
            (-23.12345678912345, unt.R8),
            ("test1234", unt.C8),
            ("test1234", "C016"),
            (23.12345678912345, "R008*100"),
            (2345, "U002*20"),
        ]
        EXPECTED_RESULTS = [
            b"\x29\x09",
            b"\x44\x55",
            b"\xd7\xfc\xb8\x41",
            b"\x1f\xc1\x37\xdd\x9a\x1f\x37\xc0",
            b"test1234",
            b"test1234        ",
            b'\xe0\x8e\xd3\xfc\xb0\x10\xa2@',
            b'4\xb7',
        ]
        for i, inp in enumerate(INPUTS):
            val, att = inp
            res = val2bytes(val, att)
            self.assertEqual(res, EXPECTED_RESULTS[i])

    def testVal2BytesBadType(self):
        with self.assertRaisesRegex(
            TypeError,
            "Attribute type U002 value xxx must be <class 'int'>, not <class 'str'>",
        ):
            res = val2bytes("xxx", "U002")

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
            (b'\xe0\x8e\xd3\xfc\xb0\x10\xa2@', "R008*100"),
        ]
        EXPECTED_RESULTS = [
            2345,
            b"\x44\x55",
            23.12345678,
            -23.12345678912345,
            "test1234",
            23.123456789123,
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
            "C016",
        ]
        EXPECTED_RESULTS = [
            0,
            b"\x00\x00",
            0.0,
            0.0,
            "        ",
            "                ",
        ]
        for i, att in enumerate(INPUTS):
            res = nomval(att)
            self.assertEqual(res, EXPECTED_RESULTS[i])

    def testNomValInvalid(self):
        with self.assertRaisesRegex(une.UNITypeError, "Unknown attribute type Y002"):
            res = nomval("Y002")

    def testattsiz(self):  # test attsiz
        self.assertEqual(attsiz(CV), -1)
        self.assertEqual(attsiz("C032"), 32)

    def testescapeall(self):
        EXPECTED_RESULT = "b'\\x68\\x65\\x72\\x65\\x61\\x72\\x65\\x73\\x6f\\x6d\\x65\\x63\\x68\\x61\\x72\\x73'"
        val = b"herearesomechars"
        res = escapeall(val)
        print(res)
        self.assertEqual(res, EXPECTED_RESULT)

    def testutc2wnotow(self):
        dat = datetime(2026, 1, 28, 9, 34, 12, 234000, tzinfo=timezone.utc)
        wno, tow, ls = utc2wnotow(dat)
        # print(wno, tow, ls)
        self.assertEqual((wno, tow), (2403, 293670234))
        wno, tow, ls = utc2wnotow()
        # print(wno, tow, ls)
        self.assertIsInstance(wno, int)
        self.assertIsInstance(tow, int)
        self.assertIsInstance(ls, int)

    def testheader2bytes(self):
        t = header2bytes(msgid=17, length=308, cpuidle=0, wno=2406, tow=34675834)
        print(t)
        self.assertEqual(
            t,
            b"\x00\x11\x004\x01\x01\x00f\tz\x1c\x11\x02\x00\x00\x00\x00\x00\x00\x00\x00",
        )
        self.assertEqual(len(t), 21)
        t = header2bytes(17, 308, 0, 1, 1, 2402, 34675834, 1, 18, 23)
        print(t)
        self.assertEqual(
            t,
            b"\x00\x11\x004\x01\x01\x01b\tz\x1c\x11\x02\x01\x00\x00\x00\x00\x12\x17\x00",
        )
        self.assertEqual(len(t), 21)
        t = header2bytes(msgid=17, length=308)  # wno and tow default to now
        self.assertEqual(len(t), 21)

    def testheader2vals(self):
        v = header2vals(
            b"\x00\x11\x004\x01\x01\x00f\tz\x1c\x11\x02\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        # print(v)
        self.assertEqual(v, (0, 17, 308, 1, 0, 2406, 34675834, 0, 0, 0, 0))
        v = header2vals(
            b"\x00\x11\x004\x01\x01\x01b\tz\x1c\x11\x02\x01\x00\x00\x00\x00\x12\x17\x00"
        )
        # print(v)
        self.assertEqual(v, (0, 17, 308, 1, 1, 2402, 34675834, 1, 0, 18, 23))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
