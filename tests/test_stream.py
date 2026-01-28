"""
Stream method tests using actual receiver binary outputs for pyqcg.QCGReader

Created on 6 Oct 2025

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import sys
import os
import unittest
from io import StringIO, BytesIO
from logging import ERROR

from pyunigps import (
    UNIReader,
    UNIMessage,
    SET,
    GET,
    POLL,
    SETPOLL,
    UNI_HDR,
    VALCKSUM,
    VALNONE,
    ERR_RAISE,
    NMEA_PROTOCOL,
    RTCM3_PROTOCOL,
    UNI_PROTOCOL,
    UNIMessageError,
    UNIParseError,
    UNIStreamError,
)
import pyunigps.unitypes_core as qgt

DIRNAME = os.path.dirname(__file__)


class StreamTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def catchio(self):
        """
        Capture stdout as string.
        """

        self._saved_stdout = sys.stdout
        self._strout = StringIO()
        sys.stdout = self._strout

    def restoreio(self) -> str:
        """
        Return captured output and restore stdout.
        """

        sys.stdout = self._saved_stdout
        return self._strout.getvalue().strip()

    def testparse(self):
        DATA= [
            b"\xaa\x44\xb5\x00\x00\x12\x05\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x01\x02\x03\x04\x05\x83\xbe\x6d\x8f",
            b"\xaa\x44\xb5\x00\x00\x14\x07\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x01\x02\x03\x04\x05\x06\x07\xa7\x13\xf1\x5b"
            ]
        EXPECTED_PARSED = [
            "<UNI(TEST12, data=197121, mode=1284)>",
            "<UNI(TEST14, data=197121, mode=1284, status=1798)>",
            ]
        stream = b""
        for msg in DATA:
            stream += msg
        unr = UNIReader(BytesIO(stream))
        i = 0
        for raw, parsed in unr:
            # print(f'"{parsed}",')
            self.assertEqual(str(parsed), EXPECTED_PARSED[i])
            i += 1
        self.assertEqual(i, len(DATA))
    

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
