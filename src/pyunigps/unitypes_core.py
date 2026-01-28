"""
UNI Protocol core globals, constants, datatypes and message identifiers.

Created on 26 Jan 2026

Information sourced from public domain Unicore UM980 Interface Specifications © 2023, Unicore
https://www.ardusimple.com/wp-content/uploads/2023/04/Unicore-Reference-Commands-Manual-For-N4-High-Precision-Products_V2_EN_R1.4-1.pdf

:author: semuadmin (Steve Smith)
"""

UNI_HDR = b"\xaa\x44\xb5"
"""UNI message header"""
GET = 0
"""GET (receive, response) message types"""
SET = 1
"""SET (command) message types"""
POLL = 2
"""POLL (query) message types"""
SETPOLL = 3
"""SETPOLL (SET or POLL) message types"""
VALNONE = 0
"""Do not validate checksum"""
VALCKSUM = 1
"""Validate checksum"""
NMEA_PROTOCOL = 1
"""NMEA Protocol"""
UNI_PROTOCOL = 2
"""UNI Protocol"""
RTCM3_PROTOCOL = 4
"""RTCM3 Protocol"""
ERR_RAISE = 2
"""Raise error and quit"""
ERR_LOG = 1
"""Log errors"""
ERR_IGNORE = 0
"""Ignore errors"""
SCALROUND = 12  # number of dp to round scaled attributes to

# **************************************************
# THESE ARE THE UNI PROTOCOL PAYLOAD ATTRIBUTE TYPES
# **************************************************
C8 = "C008"  # 8 byte haracter string
C10 = "C010"  # 10 byte character string
CV = "CXXX"  # variable length character string
R4 = "R004"  # single precision float 4 [-1*2^127,2^127]
R8 = "R008"  # double precision float 8 [-1*2^1023,2^1023]
S1 = "S001"  # signed char 1 [-128,127]
S2 = "S002"  # signed short int 2 [-32768,32767]
S4 = "S004"  # signed int 4 [-2147483648,2147483647]
S8 = "S008"  # signed long long int 8 [-2^63,2^63-1]
U1 = "U001"  # unsigned char 1 [0,255]
U2 = "U002"  # unsigned short int 2 [0,65535]
U3 = "U003"  # unsigned short int 3
U4 = "U004"  # unsigned int 4 [0,4294967295]
U5 = "U005"  # unsigned int 5
U6 = "U006"  # unsigned int 6
U8 = "U008"  # unsigned long long int 8 [0,2^64-1]
U10 = "U010"  # unsigned long long int 10
U15 = "U015"  # unsigned long long int 15
U16 = "U016"  # unsigned long long int 16
U17 = "U017"  # unsigned long long int 17
X1 = "X001"  # 8 bits field 1 Bit 7-0
X2 = "X002"  # 16 bits field 2 Bit 15-0
X4 = "X004"  # 32 bits field 4 Bit 31-0
X8 = "X008"  # 64 bits field 8 Bit 63-0
X61 = "X061"  # 61 bytes
X250 = "X250"  # 250 bytes

PAGE53 = "page_X_053"
VERSTR = "ver_C_018"
SNSTR = "sn_C_001"

ATTTYPE = {
    "S": type(-1),
    "R": type(1.1),
    "U": type(1),
    "X": type(b"0"),
    "C": type("X"),
}
"""Permissible attribute types"""

# ***************************************************************************
# THESE ARE THE UNI PROTOCOL CORE MESSAGE IDENTITIES
# Payloads for each of these identities are defined in the unitypes_* modules
# ***************************************************************************
UNI_MSGIDS = {
    b"\x00\x12": "TEST12",
    b"\x00\x14": "TEST14",
}
