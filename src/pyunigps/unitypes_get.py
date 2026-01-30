"""
UNI Protocol output definitions.

Created on 26 Jan 2026

Information sourced from public domain Unicore UM980 Interface Specifications © 2023, Unicore
https://www.ardusimple.com/wp-content/uploads/2023/04/Unicore-Reference-Commands-Manual-For-N4-High-Precision-Products_V2_EN_R1.4-1.pdf

:author: semuadmin (Steve Smith)
"""

from pyunigps.unitypes_core import (
    R4,
    U1,
    U2,
    U3,
    U4,
    U5,
    U6,
    U8,
    X1,
    X4,
)

UNI_PAYLOADS_GET = {
    # TODO add payload definitions...
    # TODO order alphabetically
    "VERSION": {
        "device": "C004",
        "swversion": "C033",
        "authtype": "C129",
        "psn": "C066",
        "efuseid": "C033",
        "comptime": "C043",
    },
    "OBSVM": {
        "numobs": U4,
        "group": (
            "numobs",
            {
                "sysfreq": U2,
                "prn": U2,
                "psr": U8,
                "adr": U8,
                "psrstd": [U2, 100],
                "adrstd": [U2, 10000],
                "doppfreq": R4,
                "cno": [U2, 100],
                "reserved1": U2,
                "locktime": R4,
                "trstatus": (
                    X4,
                    {
                        "reserved2": U5,
                        "svchan": U5,
                        "cpsflag": U1,
                        "reserved3": U1,
                        "psrflag": U1,
                        "reserved4": U3,
                        "gnss": U3,
                        "reserved5": U2,
                        "sigtype": U4,
                        "sigcode": U1,
                        "L2Cflag": U1,
                        "reserved6": U5,
                    },
                ),
            },
        ),
    },
    # "OBSVH": {} # duplicate of OVSVM, see below
    "OBSVMCMP": {},
    "OBSVHCMP": {},
    "OBSVBASE": {},
    "BASEINFO": {},
    "GPSION": {},
    "BD3ION": {},
    "BDSION": {},
    "GALION": {},
    "GPSUTC": {},
    "BD3UTC": {},
    "BDSUTC": {},
    "GALUTC": {},
    "GPSEPH": {},
    "QZSSEPH": {},
    "BD3EPH": {},
    "BDSEPH": {},
    "GLOEPH": {},
    "GALEPH": {},
    "IRNSSEPH": {},
    "AGRIC": {},
    "PVTSLN": {},
    "UNILOGLIST": {},
    "BESTNAV": {},
    "BESTNAVXYZ": {},
    "BESTNAVH": {},
    "BESTNAVXYZH": {},
    "BESTSAT": {},
    "ADRNAV": {},
    "ADRNAVH": {},
    "PPPNAV": {},
    "SPPNAV": {},
    "SPPNAVH": {},
    "STADOP": {},
    "STADOPH": {},
    "ADRDOP": {},
    "ADRDOPH": {},
    "PPPDOP": {},
    "SPPDOP": {},
    "SPPDOPH": {},
    "SATSINFO": {},
    "BASEPOS": {},
    "SATELLITE": {},
    "SATECEF": {},
    "RECTIME": {},
    "UNIHEADING": {},
    "UNIHEADING2": {},
    "HEADINGSTATUS": {},
    "RTKSTATUS": {},
    "AGNSSSTATUS": {},
    "RTCSTATUS": {},
    "JAMSTATUS": {},
    "FREQJAMSTATUS": {},
    "RTCMSTATUS": {},
    "HWSTATUS": {},
    "AGC": {},
    "KSXT": {},
    "INFOPART1": {},
    "INFOPART2": {},
    "MSPOS": {},
    "TROPINFO": {},
    "PPPB2BINFO1": {},
    "PPPB2BINFO2": {},
    "PPPB2BINFO3": {},
    "PPPB2BINFO4": {},
    "PPPB2BINFO5": {},
    "PPPB2BINFO6": {},
    "PPPB2BINFO7": {},
    "E6MASKBLOCK": {},
    "E6ORBITBLOCK": {},
    "E6CLOCKFULLBLOCK": {},
    "E6CLOCKSUBBLOCK": {},
    "E6CBIASBLOCK": {},
    "E6PBIASBLOCK": {},
    "BSLNENUHD2": {},
    "BSLNXYZHD2": {},
    "DOPHD2": {},
    "TEST12": {"data": U3, "mode": U2},
    "TEST14": {
        "data": U3,
        "mode": U2,
        "status": (
            X1,
            {
                "active": U4,
                "jamming": U2,
                "validpos": U2,
            },
        ),
        "numSV": U2,
        "group": (
            "numSV",
            {"svid": U2, "cno": U2},
        ),
    },
    # ********************************************************************
    # UNI nominal payload definition, used as fallback where no documented
    # payload definition is available.
    # ********************************************************************
    "UNI-NOMINAL": {
        "group": (
            "None",
            {
                "data": X1,
            },
        )
    },
}

# duplicated values
UNI_PAYLOADS_GET["OBSVH"] = UNI_PAYLOADS_GET["OBSVM"]
