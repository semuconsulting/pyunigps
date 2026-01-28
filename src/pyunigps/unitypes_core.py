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
#
# Uses nominal msgids in the 65000 range for messages which are only
# available in ASCII format
# ***************************************************************************
UNI_MSGIDS = {
    17: "VERSION",  # Version and Authorization
    12: "OBSVM",  # Observation of the Main Antenna
    13: "OBSVH",  # Observation of the 2nd Antenna
    138: "OBSVMCMP",  # Compressed Observation of the Main Antenna
    139: "OBSVHCMP",  # Compressed Observation of the 2nd Antenna
    284: "OBSVBASE",  # Observation of the Base Station
    176: "BASEINFO",  # Base Station Information
    8: "GPSION",  # GPS Ionosphere Parameters
    21: "BD3ION",  # BDS-3 Ionosphere Parameters
    4: "BDSION",  # BDS Ionosphere Parameters
    9: "GALION",  # Galileo Ionosphere Parameters
    19: "GPSUTC",  # Conversion between GPS Time and UTC
    22: "BD3UTC",  # Conversion between BDS-3 Time and UTC
    2012: "BDSUTC",  # Conversion between BDS Time and UTC
    20: "GALUTC",  # Conversion between Galileo Time and UTC
    106: "GPSEPH",  # GPS Ephemeris
    110: "QZSSEPH",  # QZSS Ephemeris
    2999: "BD3EPH",  # BDS-3 Ephemeris
    108: "BDSEPH",  # BDS Ephemeris
    107: "GLOEPH",  # GLONASS Ephemeris
    109: "GALEPH",  # Galileo Ephemeris
    112: "IRNSSEPH",  # IRNSS Ephemeris
    11276: "AGRIC",  # Position, velocity, serial no, heading and baseline information
    1021: "PVTSLN",  # Position and Heading Information
    65001: "UNILOGLIST",  # Output Log List (no binary version)
    2118: "BESTNAV",  # Best Position and Velocity
    240: "BESTNAVXYZ",  # Best Position and Velocity in ECEF
    2119: "BESTNAVH",  # Best Position and Velocity (2nd Antenna)
    242: "BESTNAVXYZH",  # Best Position and Velocity in ECEF (2nd Antenna)
    1041: "BESTSAT",  # Satellites Used in Position Solution
    142: "ADRNAV",  # RTK Position and Velocity
    2117: "ADRNAVH",  # RTK Position and Velocity (2nd Antenna)
    1026: "PPPNAV",  # Position and Velocity of PPP
    46: "SPPNAV",  # Pseudorange Position and Velocity
    2116: "SPPNAVH",  # Pseudorange Position and Velocity (2nd Antenna)
    954: "STADOP",  # DOP of BESTNAV
    2122: "STADOPH",  # DOP of BESTNAVH (2nd Antenna)
    953: "ADRDOP",  # DOP of ADRNAV
    2121: "ADRDOPH",  # DOP of ADRNAVH (2nd Antenna)
    1025: "PPPDOP",  # DOP of PPPNAV
    173: "SPPDOP",  # DOP of SPPNAV
    2120: "SPPDOPH",  # DOP of SPPNAVH (2nd Antenna)
    2124: "SATSINFO",  # Satellite Information
    49: "BASEPOS",  # Position of the Base Station
    1042: "SATELLITE",  # Visible Satellites
    2115: "SATECEF",  # Satellite Coordinates in ECEF
    102: "RECTIME",  # Time Information
    972: "UNIHEADING",  # Heading Information
    1331: "UNIHEADING2",  # Multi-Rover Heading Information
    521: "HEADINGSTATUS",  # Heading Status
    509: "RTKSTATUS",  # RTK Solution Status
    512: "AGNSSSTATUS",  # AGNSS Status
    510: "RTCSTATUS",  # RTC Initialization Status
    511: "JAMSTATUS",  # Jamming Detection
    519: "FREQJAMSTATUS",  # Frequency Jamming Status
    2125: "RTCMSTATUS",  # RTCM Data Status
    218: "HWSTATUS",  # Hardware Status
    220: "AGC",  # Automatic Gain Control
    65002: "KSXT",  # Positioning and Heading Data Output (no binary format)
    1019: "INFOPART1",  # Read user-defined information in PART1
    1020: "INFOPART2",  # Read user-defined information in PART2
    520: "MSPOS",  # Best Position of Dual Antennas
    2318: "TROPINFO",  # Zenith Tropospheric Delay
    2302: "PPPB2BINFO1",  # Information Type 1
    2304: "PPPB2BINFO2",  # Information Type 2
    2306: "PPPB2BINFO3",  # Information Type 3
    2308: "PPPB2BINFO4",  # Information Type 4
    2310: "PPPB2BINFO5",  # Information Type 5
    2312: "PPPB2BINFO6",  # Information Type 6
    2314: "PPPB2BINFO7",  # Information Type 7
    2319: "E6MASKBLOCK",  # Mask Block
    2320: "E6ORBITBLOCK",  # Orbit Corrections Block
    2321: "E6CLOCKFULLBLOCK",  # Clock Full-Set Corrections Block
    2322: "E6CLOCKSUBBLOCK",  # Clock Subset Corrections Block
    2323: "E6CBIASBLOCK",  # Code Biases Block
    2324: "E6PBIASBLOCK",  # Phase Biases Block
    1316: "BSLNENUHD2",  # Heading2 Baseline in ENU Coordinate System
    1317: "BSLNXYZHD2",  # Heading2 Baseline in XYZ Coordinate System
    1333: "DOPHD2",  # DOP of Heading2
    # TODO remove after Alpha..
    65512: "TEST12",
    65514: "TEST14",
}
