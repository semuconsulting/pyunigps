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

UNI_PAYLOADS_GET = {
    "TEST12": {"data": U3, "mode": U2},
    "TEST14": {"data": U3, "mode": U2, "status": U2},
    # ********************************************************************
    # https://www.ardusimple.com/wp-content/uploads/2023/04/Unicore-Reference-Commands-Manual-For-N4-High-Precision-Products_V2_EN_R1.4-1.pdf
    # ********************************************************************
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
