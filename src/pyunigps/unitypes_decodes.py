"""
unitypes_decodes.py

UNI Protocol decodes and enumerations.

Created on 26 Jan 2026

Information sourced from public domain Unicore UM980 Interface Specifications © 2023, Unicore
https://www.ardusimple.com/wp-content/uploads/2023/04/Unicore-Reference-Commands-Manual-For-N4-High-Precision-Products_V2_EN_R1.4-1.pdf

:author: semuadmin (Steve Smith)
"""

DEVICE = {
    0: "UNKNOWN",
    1: "UB4B0",
    2: "UM4B0",
    3: "UM480",
    4: "UM440",
    5: "UM482",
    6: "UM442",
    7: "UB482",
    8: "UT4B0",
    10: "UB362L",
    11: "UB4B0M",
    12: "UB4B0J",
    13: "UM482L",
    14: "UM4B0L",
    16: "CLAP-B",
    17: "UM982",
    18: "UM980",
    19: "UM960",
    21: "UM980A",
    23: "CLAP-C",
    24: "UM960L",
    26: "UM981",
    52: "UB9A0",
}
"""Hardware Device Code"""

GNSS = {
    0: "GPS",
    1: "GLONASS",
    2: "SBAS",
    3: "GAL",
    4: "BDS",
    5: "QZSS",
    6: "IRNSS",
    7: "Reserved",
}
"""GNSS Satellite System Code"""

POSTYPE = {
    0: "Invalid",
    1: "Single point",
    2: "Pseudorange differential",
    4: "Fixed",
    5: "Float",
    7: "Input a fixed position",
}
""" Rover Position Status"""

CALCSTATUS = {
    0: "No differential data input",
    1: "Insufficient observation at the differential source",
    2: "High latency of differential data",
    3: "Active ionosphere (valid for base station mode)",
    4: "Insufficient observation at the ROVER",
    5: "RTK solution available",
}
"""RTK Calculate Status"""
