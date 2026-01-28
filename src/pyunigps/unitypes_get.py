"""
UNI Protocol output definitions.

Created on 26 Jan 2026

Information sourced from public domain Unicore UM980 Interface Specifications © 2023, Unicore
https://www.ardusimple.com/wp-content/uploads/2023/04/Unicore-Reference-Commands-Manual-For-N4-High-Precision-Products_V2_EN_R1.4-1.pdf

:author: semuadmin (Steve Smith)
"""

# pylint: disable=too-many-lines, line-too-long, unused-import

from pyunigps.unitypes_core import (
    C8,
    C10,
    PAGE53,
    R4,
    SNSTR,
    U1,
    U2,
    U3,
    U4,
    U5,
    U6,
    U8,
    U15,
    U16,
    U17,
    VERSTR,
    X1,
    X61,
    X250,
)

# ********************************************************************
# https://www.ardusimple.com/wp-content/uploads/2023/04/Unicore-Reference-Commands-Manual-For-N4-High-Precision-Products_V2_EN_R1.4-1.pdf
# ********************************************************************
UNI_PAYLOADS_GET = {
    # TODO add payload definitions...
    # TODO order alphabetically
    "VERSION": {},
    "OBSVM": {},
    "OBSVH": {},
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
    "TEST14": {"data": U3, "mode": U2, "status": U2},
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
