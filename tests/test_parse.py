"""
Parse method tests

Created on 26 Jan 2026

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

# pylint: disable=line-too-long, invalid-name, missing-docstring, no-member

import os
import sys
import unittest
from io import BytesIO, StringIO

import pyunigps.exceptions as une
from pyunigps import (
    ERR_RAISE,
    GET,
    NMEA_PROTOCOL,
    POLL,
    RTCM3_PROTOCOL,
    UNI_PROTOCOL,
    UNI_ASCII_PROTOCOL,
    VALCKSUM,
    UNIMessage,
    UNIReader,
)
from pyunigps.unihelpers import isvalid_checksum

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
        DATA = [
            b"\xaa\x44\xb5\x00\xe8\xff\x05\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x01\x02\x03\x04\x05\xc1\xff\xd2\xaa",
            b'\xaaD\xb5\x00\xea\xff\x14\x00\x01\x00f\t\xaa\xdd\x13\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x03\x00\x08\x00"\x00\x0f\x007\x00\x17\x000\x00\xa2_\x8a\xd4',
        ]
        EXPECTED_PARSED = [
            "<UNI(TEST12, cpuidle=0, timeref=17, timestatus=34, wno=17459, tow=2289526357, version=571539609, leapsecond=68, delay=26197, data=197121, mode=1284)>",
            "<UNI(TEST14, cpuidle=0, timeref=1, timestatus=0, wno=2406, tow=34856362, version=1, leapsecond=0, delay=0, data=0, mode=0, active=1, jamming=0, validpos=1, numSV=3, svid_01=8, cno_01=34, svid_02=15, cno_02=55, svid_03=23, cno_03=48)>",
        ]
        stream = b""
        for msg in DATA:
            stream += msg
        unr = UNIReader(BytesIO(stream))
        i = 0
        for raw, parsed in unr:
            # print(f'"{parsed}",')
            self.assertEqual(str(parsed), EXPECTED_PARSED[i])
            self.assertEqual(parsed.msgmode, 0)
            self.assertEqual(parsed.unimode, "B")
            self.assertEqual(isvalid_checksum(raw), True)
            i += 1
        self.assertEqual(i, len(DATA))

    def testparseSATSINFO(self):
        DATA = [
            b"\xaaD\xb5`L\x08\xf6\x02\x01\x01\xa7\x08\x18\x03\xe3\x15\x00\x00\x00\x00\x00\x12\x10\x002\x00\x00\x00\x00+\x02.\x013\x00-\x00\x02\x00*\t\x02\x040\x00\x11\x00%\x00\x03\x00+\x0e\x03\x00'\t\x03\x05\xe1\x00\x0e\x00*\x00\x02\x00%\t\x02\x06#\x00@\x00/\x00\x03\x004\x0e\x03\x000\t\x03\tP\x00!\x00*\x00\x03\x00,\x0e\x03\x00(\t\x03\x0b,\x018\x00.\x00\x03\x002\x0e\x03\x00.\t\x03\x0c\x15\x01%\x00*\x00\x02\x00)\t\x02\x11\x86\x00\x1f\x00,\x00\x02\x00)\t\x02\x13\x82\x005\x00.\x00\x02\x00+\t\x02\x14\xe8\x00/\x00.\x00\x02\x00*\t\x02\x19<\x01\x0f\x00&\x00\x03\x00-\x0e\x03\x00(\t\x03\x1c\x00\x00\x00\x00%\x00\x02\x00\x1f\t\x02\xc2\xaa\x00\x08\x05&\x00\x03\x05)\x0e\x03\x05%\t\x03\xc3p\x00C\x05-\x00\x03\x051\x0e\x03\x05/\t\x03\xc4\x84\x00=\x05*\x00\x03\x050\x0e\x03\x05.\t\x03\xc7\xa3\x00+\x05$\x00\x03\x05.\x0e\x03\x05,\t\x03't\x00@\x01+\x00\x02\x011\x05\x027<\x01\x1e\x01+\x00\x02\x01.\x05\x024\xf2\x00\n\x01'\x00\x02\x01'\x05\x02&#\x00\x1c\x01(\x00\x02\x01)\x05\x02=]\x00\x1d\x01*\x00\x02\x01-\x05\x026\x16\x00>\x01/\x00\x02\x012\x05\x02(\xb4\x00\x1b\x01*\x00\x02\x01-\x05\x02.V\x01\x04\x01\"\x00\x02\x01'\x05\x02\x0b]\x00=\x04!\x00\x03\x044\x11\x03\x042\x15\x03*r\x00C\x04\"\x00\x04\x043\x15\x04\x040\x08\x04\x041\x0c\x04\x02\xe0\x00!\x04-\x11\x02\x04)\x15\x02\n\xd6\x004\x04\x1d\x00\x03\x04.\x11\x03\x04-\x15\x03\x1c2\x01\x1c\x04\x1d\x00\x04\x04,\x15\x04\x04)\x08\x04\x04*\x0c\x04(\xb4\x00*\x04\x1f\x00\x04\x04,\x15\x04\x04+\x08\x04\x04+\x0c\x04\x08!\x01?\x04\x1f\x00\x03\x040\x11\x03\x04.\x15\x03+\x08\x00O\x04$\x00\x04\x043\x15\x04\x04/\x08\x04\x042\x0c\x04\x07\xc5\x00.\x04\x1c\x00\x03\x04/\x11\x03\x04-\x15\x03\x15/\x00\x1e\x04\x1f\x00\x04\x04+\x15\x04\x04+\x08\x04\x04+\x0c\x04\x17\xf3\x00\x04\x04\x18\x08\x02\x04\x1e\x0c\x02\x04{\x00\x1a\x04+\x11\x02\x04)\x15\x02\x05\xf8\x00\x10\x04&\x11\x02\x04#\x15\x02\x01\x8b\x00$\x04\x1c\x00\x03\x04.\x11\x03\x04+\x15\x03\"o\x00(\x04 \x00\x04\x040\x15\x04\x04,\x08\x04\x04)\x0c\x04&=\x01J\x04#\x00\x04\x041\x15\x04\x04/\x08\x04\x041\x0c\x04\x027\x01\x12\x03'\x02\x03\x03-\x11\x03\x03+\x0c\x03\x04\x88\x00&\x03+\x02\x03\x030\x11\x03\x03.\x0c\x03\n\x00\x00\x00\x03/\x02\x03\x035\x11\x03\x032\x0c\x03\x0bE\x01?\x03+\x02\x03\x03/\x11\x03\x03-\x0c\x03\x0cG\x00-\x03*\x02\x03\x03-\x11\x03\x03*\x0c\x03\x13?\x00 \x03(\x02\x03\x03(\x11\x03\x03&\x0c\x03\x18\xcb\x00\x0f\x03%\x02\x03\x03+\x11\x03\x03(\x0c\x03\x19\x04\x01 \x03*\x02\x03\x03.\x11\x03\x03,\x0c\x03\t\xb5\x00\x07\x03%\x02\x03\x03)\x11\x03\x03'\x0c\x03$\x1e\x01\x13\x03\"\x02\x03\x03*\x11\x03\x03&\x0c\x03\x87\xcb\xe8/"
        ]
        EXPECTED_PARSED = [
            "<UNI(SATSINFO, cpuidle=96, timeref=1, timestatus=1, wno=2215, tow=367199000, version=0, leapsecond=18, delay=16, numsat=50, reserved1=0, reserved2=0, reserved3=0, l1cab1ie1=1, l2cl2b2ie5b=1, l5b3ie5al5=0, b1cl1c=1, b2ag3e6=0, b2bl2p=1, prn_01=2, azi_01=302, elev_01=51, sysstatus_01_01=0, cno_01_01=45, freqstatus_01_01=0, freqno_01_01=2, sysstatus_01_02=0, cno_01_02=42, freqstatus_01_02=9, freqno_01_02=2, prn_02=4, azi_02=48, elev_02=17, sysstatus_02_01=0, cno_02_01=37, freqstatus_02_01=0, freqno_02_01=3, sysstatus_02_02=0, cno_02_02=43, freqstatus_02_02=14, freqno_02_02=3, sysstatus_02_03=0, cno_02_03=39, freqstatus_02_03=9, freqno_02_03=3, prn_03=5, azi_03=225, elev_03=14, sysstatus_03_01=0, cno_03_01=42, freqstatus_03_01=0, freqno_03_01=2, sysstatus_03_02=0, cno_03_02=37, freqstatus_03_02=9, freqno_03_02=2, prn_04=6, azi_04=35, elev_04=64, sysstatus_04_01=0, cno_04_01=47, freqstatus_04_01=0, freqno_04_01=3, sysstatus_04_02=0, cno_04_02=52, freqstatus_04_02=14, freqno_04_02=3, sysstatus_04_03=0, cno_04_03=48, freqstatus_04_03=9, freqno_04_03=3, prn_05=9, azi_05=80, elev_05=33, sysstatus_05_01=0, cno_05_01=42, freqstatus_05_01=0, freqno_05_01=3, sysstatus_05_02=0, cno_05_02=44, freqstatus_05_02=14, freqno_05_02=3, sysstatus_05_03=0, cno_05_03=40, freqstatus_05_03=9, freqno_05_03=3, prn_06=11, azi_06=300, elev_06=56, sysstatus_06_01=0, cno_06_01=46, freqstatus_06_01=0, freqno_06_01=3, sysstatus_06_02=0, cno_06_02=50, freqstatus_06_02=14, freqno_06_02=3, sysstatus_06_03=0, cno_06_03=46, freqstatus_06_03=9, freqno_06_03=3, prn_07=12, azi_07=277, elev_07=37, sysstatus_07_01=0, cno_07_01=42, freqstatus_07_01=0, freqno_07_01=2, sysstatus_07_02=0, cno_07_02=41, freqstatus_07_02=9, freqno_07_02=2, prn_08=17, azi_08=134, elev_08=31, sysstatus_08_01=0, cno_08_01=44, freqstatus_08_01=0, freqno_08_01=2, sysstatus_08_02=0, cno_08_02=41, freqstatus_08_02=9, freqno_08_02=2, prn_09=19, azi_09=130, elev_09=53, sysstatus_09_01=0, cno_09_01=46, freqstatus_09_01=0, freqno_09_01=2, sysstatus_09_02=0, cno_09_02=43, freqstatus_09_02=9, freqno_09_02=2, prn_10=20, azi_10=232, elev_10=47, sysstatus_10_01=0, cno_10_01=46, freqstatus_10_01=0, freqno_10_01=2, sysstatus_10_02=0, cno_10_02=42, freqstatus_10_02=9, freqno_10_02=2, prn_11=25, azi_11=316, elev_11=15, sysstatus_11_01=0, cno_11_01=38, freqstatus_11_01=0, freqno_11_01=3, sysstatus_11_02=0, cno_11_02=45, freqstatus_11_02=14, freqno_11_02=3, sysstatus_11_03=0, cno_11_03=40, freqstatus_11_03=9, freqno_11_03=3, prn_12=28, azi_12=0, elev_12=0, sysstatus_12_01=0, cno_12_01=37, freqstatus_12_01=0, freqno_12_01=2, sysstatus_12_02=0, cno_12_02=31, freqstatus_12_02=9, freqno_12_02=2, prn_13=194, azi_13=170, elev_13=8, sysstatus_13_01=5, cno_13_01=38, freqstatus_13_01=0, freqno_13_01=3, sysstatus_13_02=5, cno_13_02=41, freqstatus_13_02=14, freqno_13_02=3, sysstatus_13_03=5, cno_13_03=37, freqstatus_13_03=9, freqno_13_03=3, prn_14=195, azi_14=112, elev_14=67, sysstatus_14_01=5, cno_14_01=45, freqstatus_14_01=0, freqno_14_01=3, sysstatus_14_02=5, cno_14_02=49, freqstatus_14_02=14, freqno_14_02=3, sysstatus_14_03=5, cno_14_03=47, freqstatus_14_03=9, freqno_14_03=3, prn_15=196, azi_15=132, elev_15=61, sysstatus_15_01=5, cno_15_01=42, freqstatus_15_01=0, freqno_15_01=3, sysstatus_15_02=5, cno_15_02=48, freqstatus_15_02=14, freqno_15_02=3, sysstatus_15_03=5, cno_15_03=46, freqstatus_15_03=9, freqno_15_03=3, prn_16=199, azi_16=163, elev_16=43, sysstatus_16_01=5, cno_16_01=36, freqstatus_16_01=0, freqno_16_01=3, sysstatus_16_02=5, cno_16_02=46, freqstatus_16_02=14, freqno_16_02=3, sysstatus_16_03=5, cno_16_03=44, freqstatus_16_03=9, freqno_16_03=3, prn_17=39, azi_17=116, elev_17=64, sysstatus_17_01=1, cno_17_01=43, freqstatus_17_01=0, freqno_17_01=2, sysstatus_17_02=1, cno_17_02=49, freqstatus_17_02=5, freqno_17_02=2, prn_18=55, azi_18=316, elev_18=30, sysstatus_18_01=1, cno_18_01=43, freqstatus_18_01=0, freqno_18_01=2, sysstatus_18_02=1, cno_18_02=46, freqstatus_18_02=5, freqno_18_02=2, prn_19=52, azi_19=242, elev_19=10, sysstatus_19_01=1, cno_19_01=39, freqstatus_19_01=0, freqno_19_01=2, sysstatus_19_02=1, cno_19_02=39, freqstatus_19_02=5, freqno_19_02=2, prn_20=38, azi_20=35, elev_20=28, sysstatus_20_01=1, cno_20_01=40, freqstatus_20_01=0, freqno_20_01=2, sysstatus_20_02=1, cno_20_02=41, freqstatus_20_02=5, freqno_20_02=2, prn_21=61, azi_21=93, elev_21=29, sysstatus_21_01=1, cno_21_01=42, freqstatus_21_01=0, freqno_21_01=2, sysstatus_21_02=1, cno_21_02=45, freqstatus_21_02=5, freqno_21_02=2, prn_22=54, azi_22=22, elev_22=62, sysstatus_22_01=1, cno_22_01=47, freqstatus_22_01=0, freqno_22_01=2, sysstatus_22_02=1, cno_22_02=50, freqstatus_22_02=5, freqno_22_02=2, prn_23=40, azi_23=180, elev_23=27, sysstatus_23_01=1, cno_23_01=42, freqstatus_23_01=0, freqno_23_01=2, sysstatus_23_02=1, cno_23_02=45, freqstatus_23_02=5, freqno_23_02=2, prn_24=46, azi_24=342, elev_24=4, sysstatus_24_01=1, cno_24_01=34, freqstatus_24_01=0, freqno_24_01=2, sysstatus_24_02=1, cno_24_02=39, freqstatus_24_02=5, freqno_24_02=2, prn_25=11, azi_25=93, elev_25=61, sysstatus_25_01=4, cno_25_01=33, freqstatus_25_01=0, freqno_25_01=3, sysstatus_25_02=4, cno_25_02=52, freqstatus_25_02=17, freqno_25_02=3, sysstatus_25_03=4, cno_25_03=50, freqstatus_25_03=21, freqno_25_03=3, prn_26=42, azi_26=114, elev_26=67, sysstatus_26_01=4, cno_26_01=34, freqstatus_26_01=0, freqno_26_01=4, sysstatus_26_02=4, cno_26_02=51, freqstatus_26_02=21, freqno_26_02=4, sysstatus_26_03=4, cno_26_03=48, freqstatus_26_03=8, freqno_26_03=4, sysstatus_26_04=4, cno_26_04=49, freqstatus_26_04=12, freqno_26_04=4, prn_27=2, azi_27=224, elev_27=33, sysstatus_27_01=4, cno_27_01=45, freqstatus_27_01=17, freqno_27_01=2, sysstatus_27_02=4, cno_27_02=41, freqstatus_27_02=21, freqno_27_02=2, prn_28=10, azi_28=214, elev_28=52, sysstatus_28_01=4, cno_28_01=29, freqstatus_28_01=0, freqno_28_01=3, sysstatus_28_02=4, cno_28_02=46, freqstatus_28_02=17, freqno_28_02=3, sysstatus_28_03=4, cno_28_03=45, freqstatus_28_03=21, freqno_28_03=3, prn_29=28, azi_29=306, elev_29=28, sysstatus_29_01=4, cno_29_01=29, freqstatus_29_01=0, freqno_29_01=4, sysstatus_29_02=4, cno_29_02=44, freqstatus_29_02=21, freqno_29_02=4, sysstatus_29_03=4, cno_29_03=41, freqstatus_29_03=8, freqno_29_03=4, sysstatus_29_04=4, cno_29_04=42, freqstatus_29_04=12, freqno_29_04=4, prn_30=40, azi_30=180, elev_30=42, sysstatus_30_01=4, cno_30_01=31, freqstatus_30_01=0, freqno_30_01=4, sysstatus_30_02=4, cno_30_02=44, freqstatus_30_02=21, freqno_30_02=4, sysstatus_30_03=4, cno_30_03=43, freqstatus_30_03=8, freqno_30_03=4, sysstatus_30_04=4, cno_30_04=43, freqstatus_30_04=12, freqno_30_04=4, prn_31=8, azi_31=289, elev_31=63, sysstatus_31_01=4, cno_31_01=31, freqstatus_31_01=0, freqno_31_01=3, sysstatus_31_02=4, cno_31_02=48, freqstatus_31_02=17, freqno_31_02=3, sysstatus_31_03=4, cno_31_03=46, freqstatus_31_03=21, freqno_31_03=3, prn_32=43, azi_32=8, elev_32=79, sysstatus_32_01=4, cno_32_01=36, freqstatus_32_01=0, freqno_32_01=4, sysstatus_32_02=4, cno_32_02=51, freqstatus_32_02=21, freqno_32_02=4, sysstatus_32_03=4, cno_32_03=47, freqstatus_32_03=8, freqno_32_03=4, sysstatus_32_04=4, cno_32_04=50, freqstatus_32_04=12, freqno_32_04=4, prn_33=7, azi_33=197, elev_33=46, sysstatus_33_01=4, cno_33_01=28, freqstatus_33_01=0, freqno_33_01=3, sysstatus_33_02=4, cno_33_02=47, freqstatus_33_02=17, freqno_33_02=3, sysstatus_33_03=4, cno_33_03=45, freqstatus_33_03=21, freqno_33_03=3, prn_34=21, azi_34=47, elev_34=30, sysstatus_34_01=4, cno_34_01=31, freqstatus_34_01=0, freqno_34_01=4, sysstatus_34_02=4, cno_34_02=43, freqstatus_34_02=21, freqno_34_02=4, sysstatus_34_03=4, cno_34_03=43, freqstatus_34_03=8, freqno_34_03=4, sysstatus_34_04=4, cno_34_04=43, freqstatus_34_04=12, freqno_34_04=4, prn_35=23, azi_35=243, elev_35=4, sysstatus_35_01=4, cno_35_01=24, freqstatus_35_01=8, freqno_35_01=2, sysstatus_35_02=4, cno_35_02=30, freqstatus_35_02=12, freqno_35_02=2, prn_36=4, azi_36=123, elev_36=26, sysstatus_36_01=4, cno_36_01=43, freqstatus_36_01=17, freqno_36_01=2, sysstatus_36_02=4, cno_36_02=41, freqstatus_36_02=21, freqno_36_02=2, prn_37=5, azi_37=248, elev_37=16, sysstatus_37_01=4, cno_37_01=38, freqstatus_37_01=17, freqno_37_01=2, sysstatus_37_02=4, cno_37_02=35, freqstatus_37_02=21, freqno_37_02=2, prn_38=1, azi_38=139, elev_38=36, sysstatus_38_01=4, cno_38_01=28, freqstatus_38_01=0, freqno_38_01=3, sysstatus_38_02=4, cno_38_02=46, freqstatus_38_02=17, freqno_38_02=3, sysstatus_38_03=4, cno_38_03=43, freqstatus_38_03=21, freqno_38_03=3, prn_39=34, azi_39=111, elev_39=40, sysstatus_39_01=4, cno_39_01=32, freqstatus_39_01=0, freqno_39_01=4, sysstatus_39_02=4, cno_39_02=48, freqstatus_39_02=21, freqno_39_02=4, sysstatus_39_03=4, cno_39_03=44, freqstatus_39_03=8, freqno_39_03=4, sysstatus_39_04=4, cno_39_04=41, freqstatus_39_04=12, freqno_39_04=4, prn_40=38, azi_40=317, elev_40=74, sysstatus_40_01=4, cno_40_01=35, freqstatus_40_01=0, freqno_40_01=4, sysstatus_40_02=4, cno_40_02=49, freqstatus_40_02=21, freqno_40_02=4, sysstatus_40_03=4, cno_40_03=47, freqstatus_40_03=8, freqno_40_03=4, sysstatus_40_04=4, cno_40_04=49, freqstatus_40_04=12, freqno_40_04=4, prn_41=2, azi_41=311, elev_41=18, sysstatus_41_01=3, cno_41_01=39, freqstatus_41_01=2, freqno_41_01=3, sysstatus_41_02=3, cno_41_02=45, freqstatus_41_02=17, freqno_41_02=3, sysstatus_41_03=3, cno_41_03=43, freqstatus_41_03=12, freqno_41_03=3, prn_42=4, azi_42=136, elev_42=38, sysstatus_42_01=3, cno_42_01=43, freqstatus_42_01=2, freqno_42_01=3, sysstatus_42_02=3, cno_42_02=48, freqstatus_42_02=17, freqno_42_02=3, sysstatus_42_03=3, cno_42_03=46, freqstatus_42_03=12, freqno_42_03=3, prn_43=10, azi_43=0, elev_43=0, sysstatus_43_01=3, cno_43_01=47, freqstatus_43_01=2, freqno_43_01=3, sysstatus_43_02=3, cno_43_02=53, freqstatus_43_02=17, freqno_43_02=3, sysstatus_43_03=3, cno_43_03=50, freqstatus_43_03=12, freqno_43_03=3, prn_44=11, azi_44=325, elev_44=63, sysstatus_44_01=3, cno_44_01=43, freqstatus_44_01=2, freqno_44_01=3, sysstatus_44_02=3, cno_44_02=47, freqstatus_44_02=17, freqno_44_02=3, sysstatus_44_03=3, cno_44_03=45, freqstatus_44_03=12, freqno_44_03=3, prn_45=12, azi_45=71, elev_45=45, sysstatus_45_01=3, cno_45_01=42, freqstatus_45_01=2, freqno_45_01=3, sysstatus_45_02=3, cno_45_02=45, freqstatus_45_02=17, freqno_45_02=3, sysstatus_45_03=3, cno_45_03=42, freqstatus_45_03=12, freqno_45_03=3, prn_46=19, azi_46=63, elev_46=32, sysstatus_46_01=3, cno_46_01=40, freqstatus_46_01=2, freqno_46_01=3, sysstatus_46_02=3, cno_46_02=40, freqstatus_46_02=17, freqno_46_02=3, sysstatus_46_03=3, cno_46_03=38, freqstatus_46_03=12, freqno_46_03=3, prn_47=24, azi_47=203, elev_47=15, sysstatus_47_01=3, cno_47_01=37, freqstatus_47_01=2, freqno_47_01=3, sysstatus_47_02=3, cno_47_02=43, freqstatus_47_02=17, freqno_47_02=3, sysstatus_47_03=3, cno_47_03=40, freqstatus_47_03=12, freqno_47_03=3, prn_48=25, azi_48=260, elev_48=32, sysstatus_48_01=3, cno_48_01=42, freqstatus_48_01=2, freqno_48_01=3, sysstatus_48_02=3, cno_48_02=46, freqstatus_48_02=17, freqno_48_02=3, sysstatus_48_03=3, cno_48_03=44, freqstatus_48_03=12, freqno_48_03=3, prn_49=9, azi_49=181, elev_49=7, sysstatus_49_01=3, cno_49_01=37, freqstatus_49_01=2, freqno_49_01=3, sysstatus_49_02=3, cno_49_02=41, freqstatus_49_02=17, freqno_49_02=3, sysstatus_49_03=3, cno_49_03=39, freqstatus_49_03=12, freqno_49_03=3, prn_50=36, azi_50=286, elev_50=19, sysstatus_50_01=3, cno_50_01=34, freqstatus_50_01=2, freqno_50_01=3, sysstatus_50_02=3, cno_50_02=42, freqstatus_50_02=17, freqno_50_02=3, sysstatus_50_03=3, cno_50_03=38, freqstatus_50_03=12, freqno_50_03=3)>",
        ]
        stream = b""
        for msg in DATA:
            stream += msg
        unr = UNIReader(BytesIO(stream))
        i = 0
        for raw, parsed in unr:
            # print(f'"{parsed}",')
            self.assertEqual(str(parsed), EXPECTED_PARSED[i])
            self.assertEqual(parsed.msgmode, 0)
            self.assertEqual(isvalid_checksum(raw), True)
            i += 1
        self.assertEqual(i, len(DATA))

    def testconstructTEST12(self):
        EXPECTED_RESULT = "<UNI(TEST12, cpuidle=0, timeref=1, timestatus=0, wno=2406, tow=34856362, version=1, leapsecond=0, delay=0, data=197121, mode=1284)>"
        msg = UNIMessage(
            msgid=65512,
            length=None,
            cpuidle=0,
            timeref=1,
            timestatus=0,
            wno=2406,
            tow=34856362,
            version=1,
            leapsecond=0,
            delay=0,
            checksum=None,
            payload=b"\x01\x02\x03\x04\x05",
            msgmode=GET,
            parsebitfield=1,
        )
        # print(msg)
        self.assertEqual(str(msg), EXPECTED_RESULT)
        self.assertEqual(msg.checksum, b"\xb5\x0c\xf5\x11")

        # self.assertEqual(
        #     repr(msg),
        #     "UNIMessage(65512, b'\\x01\\x00\\x66\\x09\\xaa\\xdd\\x13\\x02\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00', 5, b'\\xb5\\x0c\\xf5\\x11', 0, 0, payload=b'\\x01\\x02\\x03\\x04\\x05')"
        #     )
        self.assertEqual(str(eval(repr(msg))), EXPECTED_RESULT)
        msg = UNIMessage(
            msgid=65512,
            length=None,
            cpuidle=0,
            timeref=1,
            timestatus=0,
            wno=2406,
            tow=34856362,
            version=1,
            leapsecond=0,
            delay=0,
            checksum=None,
            data=197121,
            mode=1284,
        )
        self.assertEqual(str(msg), EXPECTED_RESULT)
        self.assertEqual(msg.checksum, b"\xb5\x0c\xf5\x11")
        # self.assertEqual(
        #     repr(msg),
        #     "UNIMessage(65512, b'\\x01\\x00\\x66\\x09\\xaa\\xdd\\x13\\x02\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00', 5, b'\\xb5\\x0c\\xf5\\x11', 0, 0, payload=b'\\x01\\x02\\x03\\x04\\x05')"
        # )
        self.assertEqual(str(eval(repr(msg))), EXPECTED_RESULT)

    def testconstructTEST14(self):
        EXPECTED_RESULT = "<UNI(TEST14, cpuidle=0, timeref=1, timestatus=0, wno=2406, tow=34856362, version=1, leapsecond=0, delay=0, data=0, mode=0, active=1, jamming=0, validpos=1, numSV=3, svid_01=8, cno_01=34, svid_02=15, cno_02=55, svid_03=23, cno_03=48)>"
        msg = UNIMessage(
            msgid=65514,
            length=None,
            cpuidle=0,
            timeref=1,
            timestatus=0,
            wno=2406,
            tow=34856362,
            version=1,
            leapsecond=0,
            delay=0,
            checksum=None,
            active=1,
            jamming=0,
            validpos=1,
            numSV=3,
            svid_01=8,
            cno_01=34,
            svid_02=15,
            cno_02=55,
            svid_03=23,
            cno_03=48,
        )
        # print(msg)
        self.assertEqual(str(msg), EXPECTED_RESULT)
        self.assertEqual(msg.checksum, b"\xa2_\x8a\xd4")
        self.assertEqual(str(eval(repr(msg))), EXPECTED_RESULT)
        msg1 = UNIReader.parse(msg.serialize())
        print(msg.serialize())
        self.assertEqual(str(msg1), EXPECTED_RESULT)

    def testconstructSATSINFO(self):
        EXPECTED_RESULT = "<UNI(SATSINFO, cpuidle=96, timeref=1, timestatus=1, wno=2215, tow=367199000, version=0, leapsecond=18, delay=16, numsat=50, reserved1=0, reserved2=0, reserved3=0, l1cab1ie1=0, l2cl2b2ie5b=0, l5b3ie5al5=0, b1cl1c=0, b2ag3e6=0, b2bl2p=0, prn_01=2, azi_01=302, elev_01=51, sysstatus_01_01=0, cno_01_01=45, freqstatus_01_01=0, freqno_01_01=2, sysstatus_01_02=0, cno_01_02=42, freqstatus_01_02=9, freqno_01_02=2, prn_02=4, azi_02=48, elev_02=17, sysstatus_02_01=0, cno_02_01=37, freqstatus_02_01=0, freqno_02_01=3, sysstatus_02_02=0, cno_02_02=43, freqstatus_02_02=14, freqno_02_02=3, sysstatus_02_03=0, cno_02_03=39, freqstatus_02_03=9, freqno_02_03=3, prn_03=5, azi_03=225, elev_03=14, sysstatus_03_01=0, cno_03_01=42, freqstatus_03_01=0, freqno_03_01=2, sysstatus_03_02=0, cno_03_02=37, freqstatus_03_02=9, freqno_03_02=2, prn_04=6, azi_04=35, elev_04=64, sysstatus_04_01=0, cno_04_01=47, freqstatus_04_01=0, freqno_04_01=3, sysstatus_04_02=0, cno_04_02=52, freqstatus_04_02=14, freqno_04_02=3, sysstatus_04_03=0, cno_04_03=48, freqstatus_04_03=9, freqno_04_03=3, prn_05=9, azi_05=80, elev_05=33, sysstatus_05_01=0, cno_05_01=42, freqstatus_05_01=0, freqno_05_01=3, sysstatus_05_02=0, cno_05_02=44, freqstatus_05_02=14, freqno_05_02=3, sysstatus_05_03=0, cno_05_03=40, freqstatus_05_03=9, freqno_05_03=3, prn_06=11, azi_06=300, elev_06=56, sysstatus_06_01=0, cno_06_01=46, freqstatus_06_01=0, freqno_06_01=3, sysstatus_06_02=0, cno_06_02=50, freqstatus_06_02=14, freqno_06_02=3, sysstatus_06_03=0, cno_06_03=46, freqstatus_06_03=9, freqno_06_03=3, prn_07=12, azi_07=277, elev_07=37, sysstatus_07_01=0, cno_07_01=42, freqstatus_07_01=0, freqno_07_01=2, sysstatus_07_02=0, cno_07_02=41, freqstatus_07_02=9, freqno_07_02=2, prn_08=17, azi_08=134, elev_08=31, sysstatus_08_01=0, cno_08_01=44, freqstatus_08_01=0, freqno_08_01=2, sysstatus_08_02=0, cno_08_02=41, freqstatus_08_02=9, freqno_08_02=2, prn_09=19, azi_09=130, elev_09=53, sysstatus_09_01=0, cno_09_01=46, freqstatus_09_01=0, freqno_09_01=2, sysstatus_09_02=0, cno_09_02=43, freqstatus_09_02=9, freqno_09_02=2, prn_10=20, azi_10=232, elev_10=47, sysstatus_10_01=0, cno_10_01=46, freqstatus_10_01=0, freqno_10_01=2, sysstatus_10_02=0, cno_10_02=42, freqstatus_10_02=9, freqno_10_02=2, prn_11=25, azi_11=316, elev_11=15, sysstatus_11_01=0, cno_11_01=38, freqstatus_11_01=0, freqno_11_01=3, sysstatus_11_02=0, cno_11_02=45, freqstatus_11_02=14, freqno_11_02=3, sysstatus_11_03=0, cno_11_03=40, freqstatus_11_03=9, freqno_11_03=3, prn_12=28, azi_12=0, elev_12=0, sysstatus_12_01=0, cno_12_01=37, freqstatus_12_01=0, freqno_12_01=2, sysstatus_12_02=0, cno_12_02=31, freqstatus_12_02=9, freqno_12_02=2, prn_13=194, azi_13=170, elev_13=8, sysstatus_13_01=5, cno_13_01=38, freqstatus_13_01=0, freqno_13_01=3, sysstatus_13_02=5, cno_13_02=41, freqstatus_13_02=14, freqno_13_02=3, sysstatus_13_03=5, cno_13_03=37, freqstatus_13_03=9, freqno_13_03=3, prn_14=195, azi_14=112, elev_14=67, sysstatus_14_01=5, cno_14_01=45, freqstatus_14_01=0, freqno_14_01=3, sysstatus_14_02=5, cno_14_02=49, freqstatus_14_02=14, freqno_14_02=3, sysstatus_14_03=5, cno_14_03=47, freqstatus_14_03=9, freqno_14_03=3, prn_15=196, azi_15=132, elev_15=61, sysstatus_15_01=5, cno_15_01=42, freqstatus_15_01=0, freqno_15_01=3, sysstatus_15_02=5, cno_15_02=48, freqstatus_15_02=14, freqno_15_02=3, sysstatus_15_03=5, cno_15_03=46, freqstatus_15_03=9, freqno_15_03=3, prn_16=199, azi_16=163, elev_16=43, sysstatus_16_01=5, cno_16_01=36, freqstatus_16_01=0, freqno_16_01=3, sysstatus_16_02=5, cno_16_02=46, freqstatus_16_02=14, freqno_16_02=3, sysstatus_16_03=5, cno_16_03=44, freqstatus_16_03=9, freqno_16_03=3, prn_17=39, azi_17=116, elev_17=64, sysstatus_17_01=1, cno_17_01=43, freqstatus_17_01=0, freqno_17_01=2, sysstatus_17_02=1, cno_17_02=49, freqstatus_17_02=5, freqno_17_02=2, prn_18=55, azi_18=316, elev_18=30, sysstatus_18_01=1, cno_18_01=43, freqstatus_18_01=0, freqno_18_01=2, sysstatus_18_02=1, cno_18_02=46, freqstatus_18_02=5, freqno_18_02=2, prn_19=52, azi_19=242, elev_19=10, sysstatus_19_01=1, cno_19_01=39, freqstatus_19_01=0, freqno_19_01=2, sysstatus_19_02=1, cno_19_02=39, freqstatus_19_02=5, freqno_19_02=2, prn_20=38, azi_20=35, elev_20=28, sysstatus_20_01=1, cno_20_01=40, freqstatus_20_01=0, freqno_20_01=2, sysstatus_20_02=1, cno_20_02=41, freqstatus_20_02=5, freqno_20_02=2, prn_21=61, azi_21=93, elev_21=29, sysstatus_21_01=1, cno_21_01=42, freqstatus_21_01=0, freqno_21_01=2, sysstatus_21_02=1, cno_21_02=45, freqstatus_21_02=5, freqno_21_02=2, prn_22=54, azi_22=22, elev_22=62, sysstatus_22_01=1, cno_22_01=47, freqstatus_22_01=0, freqno_22_01=2, sysstatus_22_02=1, cno_22_02=50, freqstatus_22_02=5, freqno_22_02=2, prn_23=40, azi_23=180, elev_23=27, sysstatus_23_01=1, cno_23_01=42, freqstatus_23_01=0, freqno_23_01=2, sysstatus_23_02=1, cno_23_02=45, freqstatus_23_02=5, freqno_23_02=2, prn_24=46, azi_24=342, elev_24=4, sysstatus_24_01=1, cno_24_01=34, freqstatus_24_01=0, freqno_24_01=2, sysstatus_24_02=1, cno_24_02=39, freqstatus_24_02=5, freqno_24_02=2, prn_25=11, azi_25=93, elev_25=61, sysstatus_25_01=4, cno_25_01=33, freqstatus_25_01=0, freqno_25_01=3, sysstatus_25_02=4, cno_25_02=52, freqstatus_25_02=17, freqno_25_02=3, sysstatus_25_03=4, cno_25_03=50, freqstatus_25_03=21, freqno_25_03=3, prn_26=42, azi_26=114, elev_26=67, sysstatus_26_01=4, cno_26_01=34, freqstatus_26_01=0, freqno_26_01=4, sysstatus_26_02=4, cno_26_02=51, freqstatus_26_02=21, freqno_26_02=4, sysstatus_26_03=4, cno_26_03=48, freqstatus_26_03=8, freqno_26_03=4, sysstatus_26_04=4, cno_26_04=49, freqstatus_26_04=12, freqno_26_04=4, prn_27=2, azi_27=224, elev_27=33, sysstatus_27_01=4, cno_27_01=45, freqstatus_27_01=17, freqno_27_01=2, sysstatus_27_02=4, cno_27_02=41, freqstatus_27_02=21, freqno_27_02=2, prn_28=10, azi_28=214, elev_28=52, sysstatus_28_01=4, cno_28_01=29, freqstatus_28_01=0, freqno_28_01=3, sysstatus_28_02=4, cno_28_02=46, freqstatus_28_02=17, freqno_28_02=3, sysstatus_28_03=4, cno_28_03=45, freqstatus_28_03=21, freqno_28_03=3, prn_29=28, azi_29=306, elev_29=28, sysstatus_29_01=4, cno_29_01=29, freqstatus_29_01=0, freqno_29_01=4, sysstatus_29_02=4, cno_29_02=44, freqstatus_29_02=21, freqno_29_02=4, sysstatus_29_03=4, cno_29_03=41, freqstatus_29_03=8, freqno_29_03=4, sysstatus_29_04=4, cno_29_04=42, freqstatus_29_04=12, freqno_29_04=4, prn_30=40, azi_30=180, elev_30=42, sysstatus_30_01=4, cno_30_01=31, freqstatus_30_01=0, freqno_30_01=4, sysstatus_30_02=4, cno_30_02=44, freqstatus_30_02=21, freqno_30_02=4, sysstatus_30_03=4, cno_30_03=43, freqstatus_30_03=8, freqno_30_03=4, sysstatus_30_04=4, cno_30_04=43, freqstatus_30_04=12, freqno_30_04=4, prn_31=8, azi_31=289, elev_31=63, sysstatus_31_01=4, cno_31_01=31, freqstatus_31_01=0, freqno_31_01=3, sysstatus_31_02=4, cno_31_02=48, freqstatus_31_02=17, freqno_31_02=3, sysstatus_31_03=4, cno_31_03=46, freqstatus_31_03=21, freqno_31_03=3, prn_32=43, azi_32=8, elev_32=79, sysstatus_32_01=4, cno_32_01=36, freqstatus_32_01=0, freqno_32_01=4, sysstatus_32_02=4, cno_32_02=51, freqstatus_32_02=21, freqno_32_02=4, sysstatus_32_03=4, cno_32_03=47, freqstatus_32_03=8, freqno_32_03=4, sysstatus_32_04=4, cno_32_04=50, freqstatus_32_04=12, freqno_32_04=4, prn_33=7, azi_33=197, elev_33=46, sysstatus_33_01=4, cno_33_01=28, freqstatus_33_01=0, freqno_33_01=3, sysstatus_33_02=4, cno_33_02=47, freqstatus_33_02=17, freqno_33_02=3, sysstatus_33_03=4, cno_33_03=45, freqstatus_33_03=21, freqno_33_03=3, prn_34=21, azi_34=47, elev_34=30, sysstatus_34_01=4, cno_34_01=31, freqstatus_34_01=0, freqno_34_01=4, sysstatus_34_02=4, cno_34_02=43, freqstatus_34_02=21, freqno_34_02=4, sysstatus_34_03=4, cno_34_03=43, freqstatus_34_03=8, freqno_34_03=4, sysstatus_34_04=4, cno_34_04=43, freqstatus_34_04=12, freqno_34_04=4, prn_35=23, azi_35=243, elev_35=4, sysstatus_35_01=4, cno_35_01=24, freqstatus_35_01=8, freqno_35_01=2, sysstatus_35_02=4, cno_35_02=30, freqstatus_35_02=12, freqno_35_02=2, prn_36=4, azi_36=123, elev_36=26, sysstatus_36_01=4, cno_36_01=43, freqstatus_36_01=17, freqno_36_01=2, sysstatus_36_02=4, cno_36_02=41, freqstatus_36_02=21, freqno_36_02=2, prn_37=5, azi_37=248, elev_37=16, sysstatus_37_01=4, cno_37_01=38, freqstatus_37_01=17, freqno_37_01=2, sysstatus_37_02=4, cno_37_02=35, freqstatus_37_02=21, freqno_37_02=2, prn_38=1, azi_38=139, elev_38=36, sysstatus_38_01=4, cno_38_01=28, freqstatus_38_01=0, freqno_38_01=3, sysstatus_38_02=4, cno_38_02=46, freqstatus_38_02=17, freqno_38_02=3, sysstatus_38_03=4, cno_38_03=43, freqstatus_38_03=21, freqno_38_03=3, prn_39=34, azi_39=111, elev_39=40, sysstatus_39_01=4, cno_39_01=32, freqstatus_39_01=0, freqno_39_01=4, sysstatus_39_02=4, cno_39_02=48, freqstatus_39_02=21, freqno_39_02=4, sysstatus_39_03=4, cno_39_03=44, freqstatus_39_03=8, freqno_39_03=4, sysstatus_39_04=4, cno_39_04=41, freqstatus_39_04=12, freqno_39_04=4, prn_40=38, azi_40=317, elev_40=74, sysstatus_40_01=4, cno_40_01=35, freqstatus_40_01=0, freqno_40_01=4, sysstatus_40_02=4, cno_40_02=49, freqstatus_40_02=21, freqno_40_02=4, sysstatus_40_03=4, cno_40_03=47, freqstatus_40_03=8, freqno_40_03=4, sysstatus_40_04=4, cno_40_04=49, freqstatus_40_04=12, freqno_40_04=4, prn_41=2, azi_41=311, elev_41=18, sysstatus_41_01=3, cno_41_01=39, freqstatus_41_01=2, freqno_41_01=3, sysstatus_41_02=3, cno_41_02=45, freqstatus_41_02=17, freqno_41_02=3, sysstatus_41_03=3, cno_41_03=43, freqstatus_41_03=12, freqno_41_03=3, prn_42=4, azi_42=136, elev_42=38, sysstatus_42_01=3, cno_42_01=43, freqstatus_42_01=2, freqno_42_01=3, sysstatus_42_02=3, cno_42_02=48, freqstatus_42_02=17, freqno_42_02=3, sysstatus_42_03=3, cno_42_03=46, freqstatus_42_03=12, freqno_42_03=3, prn_43=10, azi_43=0, elev_43=0, sysstatus_43_01=3, cno_43_01=47, freqstatus_43_01=2, freqno_43_01=3, sysstatus_43_02=3, cno_43_02=53, freqstatus_43_02=17, freqno_43_02=3, sysstatus_43_03=3, cno_43_03=50, freqstatus_43_03=12, freqno_43_03=3, prn_44=11, azi_44=325, elev_44=63, sysstatus_44_01=3, cno_44_01=43, freqstatus_44_01=2, freqno_44_01=3, sysstatus_44_02=3, cno_44_02=47, freqstatus_44_02=17, freqno_44_02=3, sysstatus_44_03=3, cno_44_03=45, freqstatus_44_03=12, freqno_44_03=3, prn_45=12, azi_45=71, elev_45=45, sysstatus_45_01=3, cno_45_01=42, freqstatus_45_01=2, freqno_45_01=3, sysstatus_45_02=3, cno_45_02=45, freqstatus_45_02=17, freqno_45_02=3, sysstatus_45_03=3, cno_45_03=42, freqstatus_45_03=12, freqno_45_03=3, prn_46=19, azi_46=63, elev_46=32, sysstatus_46_01=3, cno_46_01=40, freqstatus_46_01=2, freqno_46_01=3, sysstatus_46_02=3, cno_46_02=40, freqstatus_46_02=17, freqno_46_02=3, sysstatus_46_03=3, cno_46_03=38, freqstatus_46_03=12, freqno_46_03=3, prn_47=24, azi_47=203, elev_47=15, sysstatus_47_01=3, cno_47_01=37, freqstatus_47_01=2, freqno_47_01=3, sysstatus_47_02=3, cno_47_02=43, freqstatus_47_02=17, freqno_47_02=3, sysstatus_47_03=3, cno_47_03=40, freqstatus_47_03=12, freqno_47_03=3, prn_48=25, azi_48=260, elev_48=32, sysstatus_48_01=3, cno_48_01=42, freqstatus_48_01=2, freqno_48_01=3, sysstatus_48_02=3, cno_48_02=46, freqstatus_48_02=17, freqno_48_02=3, sysstatus_48_03=3, cno_48_03=44, freqstatus_48_03=12, freqno_48_03=3, prn_49=9, azi_49=181, elev_49=7, sysstatus_49_01=3, cno_49_01=37, freqstatus_49_01=2, freqno_49_01=3, sysstatus_49_02=3, cno_49_02=41, freqstatus_49_02=17, freqno_49_02=3, sysstatus_49_03=3, cno_49_03=39, freqstatus_49_03=12, freqno_49_03=3, prn_50=36, azi_50=286, elev_50=19, sysstatus_50_01=3, cno_50_01=34, freqstatus_50_01=2, freqno_50_01=3, sysstatus_50_02=3, cno_50_02=42, freqstatus_50_02=17, freqno_50_02=3, sysstatus_50_03=3, cno_50_03=38, freqstatus_50_03=12, freqno_50_03=3)>"
        hdr = (2124, 96, 1, 1, 2215, 367199000, 0, 0, 18, 16, 50, 2, 0, 0, 0, 63)
        sats = [
            (2, 302, 51, 0, 45, 0, 2, 0, 42, 9, 2),
            (4, 48, 17, 0, 37, 0, 3, 0, 43, 14, 3, 0, 39, 9, 3),
            (5, 225, 14, 0, 42, 0, 2, 0, 37, 9, 2),
            (6, 35, 64, 0, 47, 0, 3, 0, 52, 14, 3, 0, 48, 9, 3),
            (9, 80, 33, 0, 42, 0, 3, 0, 44, 14, 3, 0, 40, 9, 3),
            (11, 300, 56, 0, 46, 0, 3, 0, 50, 14, 3, 0, 46, 9, 3),
            (12, 277, 37, 0, 42, 0, 2, 0, 41, 9, 2),
            (17, 134, 31, 0, 44, 0, 2, 0, 41, 9, 2),
            (19, 130, 53, 0, 46, 0, 2, 0, 43, 9, 2),
            (20, 232, 47, 0, 46, 0, 2, 0, 42, 9, 2),
            (25, 316, 15, 0, 38, 0, 3, 0, 45, 14, 3, 0, 40, 9, 3),
            (28, 0, 0, 0, 37, 0, 2, 0, 31, 9, 2),
            (194, 170, 8, 5, 38, 0, 3, 5, 41, 14, 3, 5, 37, 9, 3),
            (195, 112, 67, 5, 45, 0, 3, 5, 49, 14, 3, 5, 47, 9, 3),
            (196, 132, 61, 5, 42, 0, 3, 5, 48, 14, 3, 5, 46, 9, 3),
            (199, 163, 43, 5, 36, 0, 3, 5, 46, 14, 3, 5, 44, 9, 3),
            (39, 116, 64, 1, 43, 0, 2, 1, 49, 5, 2),
            (55, 316, 30, 1, 43, 0, 2, 1, 46, 5, 2),
            (52, 242, 10, 1, 39, 0, 2, 1, 39, 5, 2),
            (38, 35, 28, 1, 40, 0, 2, 1, 41, 5, 2),
            (61, 93, 29, 1, 42, 0, 2, 1, 45, 5, 2),
            (54, 22, 62, 1, 47, 0, 2, 1, 50, 5, 2),
            (40, 180, 27, 1, 42, 0, 2, 1, 45, 5, 2),
            (46, 342, 4, 1, 34, 0, 2, 1, 39, 5, 2),
            (11, 93, 61, 4, 33, 0, 3, 4, 52, 17, 3, 4, 50, 21, 3),
            (42, 114, 67, 4, 34, 0, 4, 4, 51, 21, 4, 4, 48, 8, 4, 4, 49, 12, 4),
            (2, 224, 33, 4, 45, 17, 2, 4, 41, 21, 2),
            (10, 214, 52, 4, 29, 0, 3, 4, 46, 17, 3, 4, 45, 21, 3),
            (28, 306, 28, 4, 29, 0, 4, 4, 44, 21, 4, 4, 41, 8, 4, 4, 42, 12, 4),
            (40, 180, 42, 4, 31, 0, 4, 4, 44, 21, 4, 4, 43, 8, 4, 4, 43, 12, 4),
            (8, 289, 63, 4, 31, 0, 3, 4, 48, 17, 3, 4, 46, 21, 3),
            (43, 8, 79, 4, 36, 0, 4, 4, 51, 21, 4, 4, 47, 8, 4, 4, 50, 12, 4),
            (7, 197, 46, 4, 28, 0, 3, 4, 47, 17, 3, 4, 45, 21, 3),
            (21, 47, 30, 4, 31, 0, 4, 4, 43, 21, 4, 4, 43, 8, 4, 4, 43, 12, 4),
            (23, 243, 4, 4, 24, 8, 2, 4, 30, 12, 2),
            (4, 123, 26, 4, 43, 17, 2, 4, 41, 21, 2),
            (5, 248, 16, 4, 38, 17, 2, 4, 35, 21, 2),
            (1, 139, 36, 4, 28, 0, 3, 4, 46, 17, 3, 4, 43, 21, 3),
            (34, 111, 40, 4, 32, 0, 4, 4, 48, 21, 4, 4, 44, 8, 4, 4, 41, 12, 4),
            (38, 317, 74, 4, 35, 0, 4, 4, 49, 21, 4, 4, 47, 8, 4, 4, 49, 12, 4),
            (2, 311, 18, 3, 39, 2, 3, 3, 45, 17, 3, 3, 43, 12, 3),
            (4, 136, 38, 3, 43, 2, 3, 3, 48, 17, 3, 3, 46, 12, 3),
            (10, 0, 0, 3, 47, 2, 3, 3, 53, 17, 3, 3, 50, 12, 3),
            (11, 325, 63, 3, 43, 2, 3, 3, 47, 17, 3, 3, 45, 12, 3),
            (12, 71, 45, 3, 42, 2, 3, 3, 45, 17, 3, 3, 42, 12, 3),
            (19, 63, 32, 3, 40, 2, 3, 3, 40, 17, 3, 3, 38, 12, 3),
            (24, 203, 15, 3, 37, 2, 3, 3, 43, 17, 3, 3, 40, 12, 3),
            (25, 260, 32, 3, 42, 2, 3, 3, 46, 17, 3, 3, 44, 12, 3),
            (9, 181, 7, 3, 37, 2, 3, 3, 41, 17, 3, 3, 39, 12, 3),
            (36, 286, 19, 3, 34, 2, 3, 3, 42, 17, 3, 3, 38, 12, 3),
        ]

        pre = {
            "msgid": hdr[0],
            "length": None,
            "cpuidle": hdr[1],
            "timeref": hdr[2],
            "timestatus": hdr[3],
            "wno": hdr[4],
            "tow": hdr[5],
            "version": hdr[6],
            "leapsecond": hdr[8],
            "delay": hdr[9],
            "numsat": hdr[10],
            "version": hdr[11],
            "reserved1": hdr[12],
            "reserved2": hdr[13],
            "reserved3": hdr[14],
            "L1B1IE1": 1,
            "L2CL2B2IE5b": 1,
            "L5B3IE5aL5": 0,
            "B1CL1C": 1,
            "B2aG3E6": 0,
            "B2bL2P": 1,
        }

        satd = {}
        for i, sat in enumerate(sats):
            prn = sat[0]
            azi = sat[1]
            elev = sat[2]
            freqno = sat[6]
            satd[f"prn_{i+1:02d}"] = prn
            satd[f"azi_{i+1:02d}"] = azi
            satd[f"elev_{i+1:02d}"] = elev
            for n in range(freqno):
                satd[f"sysstatus_{i+1:02d}_{n+1:02d}"] = sat[3 + n * 4]
                satd[f"cno_{i+1:02d}_{n+1:02d}"] = sat[4 + n * 4]
                satd[f"freqstatus_{i+1:02d}_{n+1:02d}"] = sat[5 + n * 4]
                satd[f"freqno_{i+1:02d}_{n+1:02d}"] = sat[6 + n * 4]

        args = {**pre, **satd}
        msg = UNIMessage(**args)
        print(f'"{msg}"')
        # self.assertEqual(str(msg), EXPECTED_RESULT)

    def testserialize(self):
        EXPECTED_RAW = b"\xaaD\xb5\x00\x11\x004\x01\x00\x00f\t\x8f\xf4\x0e\x02\x00\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x00R4.10Build5251                   HRPT00-S10C-P                                                                                                                    -                                                                 ffff48ffff0fffff                 2021/11/26                                 \x11t\x19\x1f"
        EXPECTED_PARSE = "<UNI(VERSION, cpuidle=0, timeref=0, timestatus=0, wno=2406, tow=34534543, version=0, leapsecond=0, delay=0, device=18, swversion=R4.10Build5251, authtype=HRPT00-S10C-P, psn=-, efuseid=ffff48ffff0fffff, comptime=2021/11/26)>"
        msg = UNIMessage(
            msgid=17,
            wno=2406,
            tow=34534543,
            device=18,  # UM980
            swversion="R4.10Build5251",
            authtype="HRPT00-S10C-P",
            psn="-",
            efuseid="ffff48ffff0fffff",
            comptime="2021/11/26",
        )
        print(msg.serialize())
        self.assertEqual(msg.serialize(), EXPECTED_RAW)
        msg = UNIReader.parse(msg.serialize())
        print(msg)
        self.assertEqual(str(msg), EXPECTED_PARSE)
        self.assertEqual(str(eval(repr(msg))), str(msg))

    def testimmutable(self):
        msg = UNIMessage(
            msgid=17,
            timeinfo=b"\x00" * 16,
            device=18,  # UM980
            swversion="R4.10Build5251",
            authtype="HRPT00-S10C-P",
            psn="-",
            efuseid="ffff48ffff0fffff",
            comptime="2021/11/26",
        )
        with self.assertRaisesRegex(
            une.UNIMessageError,
            "Object is immutable. Updates to device not permitted after initialisation.",
        ):
            msg.device = 18

    def testrtcm(self):  # test RTCM parsing
        EXPECTED_RESULTS = (
            "<NMEA(GNGLL, field_01=3203.94995, field_02=N, field_03=03446.42914, field_04=E, field_05=084158.00, field_06=A, field_07=D)>",
            "<RTCM(1005, DF002=1005, DF003=0, DF021=0, DF022=1, DF023=1, DF024=1, DF141=0, DF025=4444030.802800001, DF142=1, DF001_1=0, DF026=3085671.2349, DF364=0, DF027=3366658.256)>",
            "<RTCM(4072, DF002=4072, Not_Yet_Implemented)>",
            "<RTCM(1077, DF002=1077, DF003=0, DF004=204137001, DF393=1, DF409=0, DF001_7=0, DF411=0, DF412=0, DF417=0, DF418=0, DF394=760738918298550272, NSat=10, DF395=1073807360, NSig=2, DF396=1044459, NCell=17, PRN_01=005, PRN_02=007, PRN_03=009, PRN_04=013, PRN_05=014, PRN_06=015, PRN_07=017, PRN_08=019, PRN_09=020, PRN_10=030, DF397_01=75, DF397_02=75, DF397_03=81, DF397_04=72, DF397_05=67, DF397_06=80, DF397_07=75, DF397_08=82, DF397_09=75, DF397_10=71, ExtSatInfo_01=0, ExtSatInfo_02=0, ExtSatInfo_03=0, ExtSatInfo_04=0, ExtSatInfo_05=0, ExtSatInfo_06=0, ExtSatInfo_07=0, ExtSatInfo_08=0, ExtSatInfo_09=0, ExtSatInfo_10=0, DF398_01=0.005859375, DF398_02=0.5341796875, DF398_03=0.7626953125, DF398_04=0.138671875, DF398_05=0.5498046875, DF398_06=0.11328125, DF398_07=0.8037109375, DF398_08=0.1025390625, DF398_09=0.521484375, DF398_10=0.345703125, DF399_01=-178, DF399_02=-304, DF399_03=-643, DF399_04=477, DF399_05=-52, DF399_06=645, DF399_07=529, DF399_08=643, DF399_09=-428, DF399_10=-181, CELLPRN_01=005, CELLSIG_01=1C, CELLPRN_02=005, CELLSIG_02=2L, CELLPRN_03=007, CELLSIG_03=1C, CELLPRN_04=007, CELLSIG_04=2L, CELLPRN_05=009, CELLSIG_05=1C, CELLPRN_06=009, CELLSIG_06=2L, CELLPRN_07=013, CELLSIG_07=1C, CELLPRN_08=014, CELLSIG_08=1C, CELLPRN_09=014, CELLSIG_09=2L, CELLPRN_10=015, CELLSIG_10=1C, CELLPRN_11=015, CELLSIG_11=2L, CELLPRN_12=017, CELLSIG_12=1C, CELLPRN_13=017, CELLSIG_13=2L, CELLPRN_14=019, CELLSIG_14=1C, CELLPRN_15=020, CELLSIG_15=1C, CELLPRN_16=030, CELLSIG_16=1C, CELLPRN_17=030, CELLSIG_17=2L, DF405_01=0.00014309026300907135, DF405_02=0.00014183297753334045, DF405_03=0.0003883279860019684, DF405_04=0.00038741156458854675, DF405_05=-0.0004838351160287857, DF405_06=-0.00046883709728717804, DF405_07=0.0003478657454252243, DF405_08=0.0002196934074163437, DF405_09=0.00021521002054214478, DF405_10=-0.00018852390348911285, DF405_11=-0.00018319115042686462, DF405_12=-0.00010087713599205017, DF405_13=-9.844452142715454e-05, DF405_14=0.00047875382006168365, DF405_15=0.00043664872646331787, DF405_16=-0.0003105681389570236, DF405_17=-0.00030865520238876343, DF406_01=0.00014193402603268623, DF406_02=0.00014339853078126907, DF406_03=0.00039040297269821167, DF406_04=0.00038743019104003906, DF406_05=-0.0004843934439122677, DF406_06=-0.00046825408935546875, DF406_07=0.0003473707474768162, DF406_08=0.00021758908405900002, DF406_09=0.00021597417071461678, DF406_10=-0.00018658116459846497, DF406_11=-0.00018350128084421158, DF406_12=-9.993184357881546e-05, DF406_13=-9.724870324134827e-05, DF406_14=0.0004128236323595047, DF406_15=0.0004355977289378643, DF406_16=-0.0003112703561782837, DF406_17=-0.00030898721888661385, DF407_01=341, DF407_02=341, DF407_03=341, DF407_04=341, DF407_05=341, DF407_06=341, DF407_07=341, DF407_08=341, DF407_09=341, DF407_10=341, DF407_11=341, DF407_12=341, DF407_13=341, DF407_14=295, DF407_15=341, DF407_16=341, DF407_17=341, DF420_01=0, DF420_02=0, DF420_03=0, DF420_04=0, DF420_05=0, DF420_06=0, DF420_07=0, DF420_08=0, DF420_09=0, DF420_10=0, DF420_11=0, DF420_12=0, DF420_13=0, DF420_14=0, DF420_15=0, DF420_16=0, DF420_17=0, DF408_01=45.0, DF408_02=38.0, DF408_03=43.0, DF408_04=39.0, DF408_05=39.0, DF408_06=37.0, DF408_07=45.0, DF408_08=46.0, DF408_09=46.0, DF408_10=39.0, DF408_11=34.0, DF408_12=45.0, DF408_13=38.0, DF408_14=31.0, DF408_15=45.0, DF408_16=46.0, DF408_17=41.0, DF404_01=-0.9231, DF404_02=-0.9194, DF404_03=-0.8321000000000001, DF404_04=-0.8326, DF404_05=-0.4107, DF404_06=-0.4072, DF404_07=0.2451, DF404_08=-0.0693, DF404_09=-0.0684, DF404_10=0.9390000000000001, DF404_11=0.9417000000000001, DF404_12=0.2384, DF404_13=0.2416, DF404_14=0.6636000000000001, DF404_15=-0.9556, DF404_16=-0.21480000000000002, DF404_17=-0.2174)>",
            "<RTCM(1087, DF002=1087, DF003=0, DF416=2, DF034=42119001, DF393=1, DF409=0, DF001_7=0, DF411=0, DF412=0, DF417=0, DF418=0, DF394=4039168114821169152, NSat=7, DF395=1090519040, NSig=2, DF396=16382, NCell=13, PRN_01=003, PRN_02=004, PRN_03=005, PRN_04=013, PRN_05=014, PRN_06=015, PRN_07=023, DF397_01=69, DF397_02=64, DF397_03=73, DF397_04=76, DF397_05=66, DF397_06=70, DF397_07=78, DF419_01=12, DF419_02=13, DF419_03=8, DF419_04=5, DF419_05=0, DF419_06=7, DF419_07=10, DF398_01=0.6337890625, DF398_02=0.3427734375, DF398_03=0.25390625, DF398_04=0.310546875, DF398_05=0.5126953125, DF398_06=0.8271484375, DF398_07=0.8837890625, DF399_01=-665, DF399_02=29, DF399_03=672, DF399_04=-573, DF399_05=-211, DF399_06=312, DF399_07=317, CELLPRN_01=003, CELLSIG_01=1C, CELLPRN_02=003, CELLSIG_02=2C, CELLPRN_03=004, CELLSIG_03=1C, CELLPRN_04=004, CELLSIG_04=2C, CELLPRN_05=005, CELLSIG_05=1C, CELLPRN_06=005, CELLSIG_06=2C, CELLPRN_07=013, CELLSIG_07=1C, CELLPRN_08=013, CELLSIG_08=2C, CELLPRN_09=014, CELLSIG_09=1C, CELLPRN_10=014, CELLSIG_10=2C, CELLPRN_11=015, CELLSIG_11=1C, CELLPRN_12=015, CELLSIG_12=2C, CELLPRN_13=023, CELLSIG_13=1C, DF405_01=0.00024936161935329437, DF405_02=0.0002511627972126007, DF405_03=-4.678964614868164e-05, DF405_04=-5.141831934452057e-05, DF405_05=1.1144205927848816e-05, DF405_06=2.15042382478714e-05, DF405_07=0.00047079287469387054, DF405_08=0.0004794951528310776, DF405_09=-0.0003879182040691376, DF405_10=-0.00037603825330734253, DF405_11=0.0002771839499473572, DF405_12=0.0002871435135602951, DF405_13=-0.00023611821234226227, DF406_01=0.00024937279522418976, DF406_02=0.00025077443569898605, DF406_03=-4.834495484828949e-05, DF406_04=-5.1246024668216705e-05, DF406_05=1.1149328202009201e-05, DF406_06=2.1803192794322968e-05, DF406_07=0.00047026341781020164, DF406_08=0.0004848274402320385, DF406_09=-0.0003876127302646637, DF406_10=-0.0003757951781153679, DF406_11=0.0002778824418783188, DF406_12=0.0002880701795220375, DF406_13=-0.00023698341101408005, DF407_01=341, DF407_02=341, DF407_03=340, DF407_04=340, DF407_05=341, DF407_06=341, DF407_07=340, DF407_08=341, DF407_09=341, DF407_10=341, DF407_11=341, DF407_12=341, DF407_13=340, DF420_01=0, DF420_02=0, DF420_03=0, DF420_04=0, DF420_05=0, DF420_06=0, DF420_07=0, DF420_08=0, DF420_09=0, DF420_10=0, DF420_11=0, DF420_12=0, DF420_13=0, DF408_01=47.0, DF408_02=40.0, DF408_03=47.0, DF408_04=42.0, DF408_05=47.0, DF408_06=39.0, DF408_07=36.0, DF408_08=33.0, DF408_09=48.0, DF408_10=43.0, DF408_11=48.0, DF408_12=40.0, DF408_13=41.0, DF404_01=-0.8193, DF404_02=-0.8173, DF404_03=0.8539, DF404_04=0.8501000000000001, DF404_05=0.7333000000000001, DF404_06=0.7311000000000001, DF404_07=-0.24930000000000002, DF404_08=-0.2543, DF404_09=-0.21580000000000002, DF404_10=-0.21780000000000002, DF404_11=0.3924, DF404_12=0.3947, DF404_13=0.6146)>",
            "<RTCM(1097, DF002=1097, DF003=0, DF248=204137001, DF393=1, DF409=0, DF001_7=0, DF411=0, DF412=0, DF417=0, DF418=0, DF394=216181732825628672, NSat=5, DF395=1073872896, NSig=2, DF396=1023, NCell=10, PRN_01=007, PRN_02=008, PRN_03=021, PRN_04=027, PRN_05=030, DF397_01=79, DF397_02=84, DF397_03=89, DF397_04=78, DF397_05=83, ExtSatInfo_01=0, ExtSatInfo_02=0, ExtSatInfo_03=0, ExtSatInfo_04=0, ExtSatInfo_05=0, DF398_01=0.15625, DF398_02=0.2509765625, DF398_03=0.3544921875, DF398_04=0.37109375, DF398_05=0.259765625, DF399_01=-198, DF399_02=-516, DF399_03=423, DF399_04=63, DF399_05=-384, CELLPRN_01=007, CELLSIG_01=1C, CELLPRN_02=007, CELLSIG_02=7Q, CELLPRN_03=008, CELLSIG_03=1C, CELLPRN_04=008, CELLSIG_04=7Q, CELLPRN_05=021, CELLSIG_05=1C, CELLPRN_06=021, CELLSIG_06=7Q, CELLPRN_07=027, CELLSIG_07=1C, CELLPRN_08=027, CELLSIG_08=7Q, CELLPRN_09=030, CELLSIG_09=1C, CELLPRN_10=030, CELLSIG_10=7Q, DF405_01=-4.5398250222206116e-05, DF405_02=-2.8252601623535156e-05, DF405_03=-0.00034597329795360565, DF405_04=-0.0003268253058195114, DF405_05=0.0004809703677892685, DF405_06=0.0005012489855289459, DF405_07=-0.00013696029782295227, DF405_08=-0.0001260414719581604, DF405_09=-1.8440186977386475e-05, DF405_10=-3.041699528694153e-06, DF406_01=-4.44464385509491e-05, DF406_02=-2.835458144545555e-05, DF406_03=-0.0003525479696691036, DF406_04=-0.0003263736143708229, DF406_05=0.00048203859478235245, DF406_06=0.0005008447915315628, DF406_07=-0.0001375703141093254, DF406_08=-0.00012635625898838043, DF406_09=-1.8037855625152588e-05, DF406_10=-3.2926909625530243e-06, DF407_01=341, DF407_02=341, DF407_03=341, DF407_04=341, DF407_05=341, DF407_06=341, DF407_07=341, DF407_08=341, DF407_09=341, DF407_10=341, DF420_01=0, DF420_02=0, DF420_03=0, DF420_04=0, DF420_05=0, DF420_06=0, DF420_07=0, DF420_08=0, DF420_09=0, DF420_10=0, DF408_01=46.0, DF408_02=49.0, DF408_03=41.0, DF408_04=43.0, DF408_05=43.0, DF408_06=43.0, DF408_07=45.0, DF408_08=49.0, DF408_09=43.0, DF408_10=47.0, DF404_01=-0.5806, DF404_02=-0.5831000000000001, DF404_03=-0.7947000000000001, DF404_04=-0.7943, DF404_05=0.7243, DF404_06=0.7174, DF404_07=0.5534, DF404_08=0.5545, DF404_09=-0.7726000000000001, DF404_10=-0.7733)>",
            "<RTCM(1127, DF002=1127, DF003=0, DF427=204123001, DF393=0, DF409=0, DF001_7=0, DF411=0, DF412=0, DF417=0, DF418=0, DF394=198178247981137920, NSat=10, DF395=1074003968, NSig=2, DF396=387754, NCell=11, PRN_01=007, PRN_02=009, PRN_03=010, PRN_04=020, PRN_05=023, PRN_06=028, PRN_07=032, PRN_08=037, PRN_09=040, PRN_10=043, DF397_01=129, DF397_02=132, DF397_03=126, DF397_04=75, DF397_05=81, DF397_06=84, DF397_07=78, DF397_08=74, DF397_09=130, DF397_10=86, ExtSatInfo_01=0, ExtSatInfo_02=0, ExtSatInfo_03=0, ExtSatInfo_04=0, ExtSatInfo_05=0, ExtSatInfo_06=0, ExtSatInfo_07=0, ExtSatInfo_08=0, ExtSatInfo_09=0, ExtSatInfo_10=0, DF398_01=0.1171875, DF398_02=0.4814453125, DF398_03=0.3095703125, DF398_04=0.7255859375, DF398_05=0.41015625, DF398_06=0.5703125, DF398_07=0.5595703125, DF398_08=0.322265625, DF398_09=0.578125, DF398_10=0.673828125, DF399_01=-130, DF399_02=-58, DF399_03=-81, DF399_04=32, DF399_05=-398, DF399_06=436, DF399_07=-523, DF399_08=-65, DF399_09=-182, DF399_10=79, CELLPRN_01=007, CELLSIG_01=7I, CELLPRN_02=009, CELLSIG_02=7I, CELLPRN_03=010, CELLSIG_03=2I, CELLPRN_04=010, CELLSIG_04=7I, CELLPRN_05=020, CELLSIG_05=2I, CELLPRN_06=023, CELLSIG_06=2I, CELLPRN_07=028, CELLSIG_07=2I, CELLPRN_08=032, CELLSIG_08=2I, CELLPRN_09=037, CELLSIG_09=2I, CELLPRN_10=040, CELLSIG_10=2I, CELLPRN_11=043, CELLSIG_11=2I, DF405_01=-0.0003885403275489807, DF405_02=0.00022730417549610138, DF405_03=0.0004036612808704376, DF405_04=0.00039606913924217224, DF405_05=-0.00016684085130691528, DF405_06=-4.75514680147171e-05, DF405_07=0.0003674682229757309, DF405_08=0.00026629865169525146, DF405_09=-0.0002502594143152237, DF405_10=-0.00011803768575191498, DF405_11=-0.0002937670797109604, DF406_01=-0.0003882073797285557, DF406_02=0.0002264929935336113, DF406_03=0.0004031979478895664, DF406_04=0.0003964221104979515, DF406_05=-0.00016694329679012299, DF406_06=-4.848744720220566e-05, DF406_07=0.00036971503868699074, DF406_08=0.0002654106356203556, DF406_09=-0.00025115441530942917, DF406_10=-0.00011868216097354889, DF406_11=-0.00029495684430003166, DF407_01=341, DF407_02=341, DF407_03=341, DF407_04=341, DF407_05=341, DF407_06=341, DF407_07=341, DF407_08=341, DF407_09=341, DF407_10=341, DF407_11=341, DF420_01=0, DF420_02=0, DF420_03=0, DF420_04=0, DF420_05=0, DF420_06=0, DF420_07=0, DF420_08=0, DF420_09=0, DF420_10=0, DF420_11=0, DF408_01=45.0, DF408_02=41.0, DF408_03=42.0, DF408_04=45.0, DF408_05=48.0, DF408_06=46.0, DF408_07=42.0, DF408_08=47.0, DF408_09=48.0, DF408_10=44.0, DF408_11=43.0, DF404_01=-0.5674, DF404_02=-0.612, DF404_03=-0.1384, DF404_04=-0.1332, DF404_05=0.5992000000000001, DF404_06=-0.7312000000000001, DF404_07=0.17320000000000002, DF404_08=-0.4308, DF404_09=-0.5975, DF404_10=-0.6733, DF404_11=0.6122000000000001)>",
            "<RTCM(1230, DF002=1230, DF003=0, DF421=1, DF001_3=0, DF422_1=0, DF422_2=0, DF422_3=0, DF422_4=0)>",
            "<NMEA(GNRMC, field_01=084159.00, field_02=A, field_03=3203.94995, field_04=N, field_05=03446.42914, field_06=E, field_07=0.000, field_08=, field_09=080222, field_10=, field_11=, field_12=D, field_13=V)>",
        )

        i = 0
        with open(os.path.join(DIRNAME, "pygpsdata_mixed_rtcm3.log"), "rb") as stream:
            ubr = UNIReader(
                stream,
                protfilter=UNI_PROTOCOL | RTCM3_PROTOCOL | NMEA_PROTOCOL,
                parsing=True,
                parsebitfield=1,
                validate=VALCKSUM,
                msgmode=POLL,
                quitonerror=ERR_RAISE,
            )
            for raw, parsed in ubr:
                # print(f'"{parsed}",')
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1
            self.assertEqual(i, len(EXPECTED_RESULTS))

    def testparseascii(self): # TODO replace with correct results when ascii parsing implemented
        EXPECTED_RESULTS = (
            "<UNI(VERSION, cpuidle=94, timeref=0, timestatus=1, wno=2190, tow=117325000, version=0, leapsecond=18, delay=160, device=0, swversion=, authtype=, psn=, efuseid=, comptime=)>",
            "<UNI(BD3ION, cpuidle=89, timeref=0, timestatus=1, wno=2190, tow=371265000, version=0, leapsecond=18, delay=22, a1=0.0, a2=0.0, a3=0.0, a4=0.0, a5=0.0, a6=0.0, a7=0.0, a8=0.0, a9=0.0, reserved1=0)>",
            "<UNI(IRNSSEPH, cpuidle=87, timeref=0, timestatus=1, wno=2305, tow=116273000, version=0, leapsecond=18, delay=31, prn=0, towc=0.0, l5health=0, iodec=0, shealth=0, week=0, reserved1=0, toe=0.0, a=0.0, deltan=0.0, m0=0.0, ecc=0.0, omega=0.0, cuc=0.0, cus=0.0, crc=0.0, crs=0.0, cic=0.0, cis=0.0, i0=0.0, idot=0.0, omega0=0.0, omegadot=0.0, reserved2=0, toc=0.0, tgd=0.0, af0=0.0, af1=0.0, af2=0.0, flag=0, n=0.0, ura=0.0)>",
            "<UNI(GALEPH, cpuidle=97, timeref=0, timestatus=1, wno=2190, tow=363656000, version=0, leapsecond=18, delay=3, satid=0, fnavreceived=0, inavreceived=0, e1bhealth=0, e5ahealth=0, e5bhealth=0, e1bdvs=0, e5advs=0, e5bdvs=0, sisa=0, reserved1=0, iodnav=0, toe=0, roota=0.0, deltan=0.0, m0=0.0, ecc=0.0, omega=0.0, cuc=0.0, cus=0.0, crc=0.0, crs=0.0, cic=0.0, cis=0.0, i0=0.0, idot=0.0, omega0=0.0, omegadot=0.0, fnavt0c=0, fnavaf0=0.0, fnavaf1=0.0, fnavaf2=0.0, inavt0c=0, inavaf0=0.0, inavaf1=0.0, inavaf2=0.0, e1e5abgd=0.0, e1e5bbgd=0.0)>",
        )

        i = 0
        with open(os.path.join(DIRNAME, "pygpsdata_uni_ascii.log"), "rb") as stream:
            ubr = UNIReader(
                stream,
                protfilter=UNI_ASCII_PROTOCOL | RTCM3_PROTOCOL | NMEA_PROTOCOL,
                parsing=True,
                parsebitfield=1,
                validate=VALCKSUM,
                quitonerror=ERR_RAISE,
            )
            for raw, parsed in ubr:
                # print(f'"{parsed}",')
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1
            self.assertEqual(i, len(EXPECTED_RESULTS))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
