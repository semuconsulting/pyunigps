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
    # TODO replace sequential nos with actual msgids...
    b"\x01\x00": "VERSION",  # Version and Authorization
    b"\x02\x00": "OBSVM",  # Observation of the Main Antenna
    b"\x03\x00": "OBSVH",  # Observation of the 2nd Antenna
    b"\x04\x00": "OBSVMCMP",  # Compressed Observation of the Main Antenna
    b"\x05\x00": "OBSVHCMP",  # Compressed Observation of the 2nd Antenna
    b"\x06\x00": "OBSVBASE",  # Observation of the Base Station
    b"\x07\x00": "BASEINFO",  # Base Station Information
    b"\x08\x00": "GPSION",  # GPS Ionosphere Parameters
    b"\x09\x00": "BD3ION",  # BDS-3 Ionosphere Parameters
    b"\x0a\x00": "BDSION",  # BDS Ionosphere Parameters
    b"\x0b\x00": "GALION",  # Galileo Ionosphere Parameters
    b"\x0c\x00": "GPSUTC",  # Conversion between GPS Time and UTC
    b"\x0d\x00": "BD3UTC",  # Conversion between BDS-3 Time and UTC
    b"\x0e\x00": "BDSUTC",  # Conversion between BDS Time and UTC
    b"\x0f\x00": "GALUTC",  # Conversion between Galileo Time and UTC
    b"\x10\x00": "GPSEPH",  # GPS Ephemeris
    b"\x11\x00": "QZSSEPH",  # QZSS Ephemeris
    b"\x12\x00": "BD3EPH",  # BDS-3 Ephemeris
    b"\x13\x00": "BDSEPH",  # BDS Ephemeris
    b"\x14\x00": "GLOEPH",  # GLONASS Ephemeris
    b"\x15\x00": "GALEPH",  # Galileo Ephemeris
    b"\x16\x00": "IRNSSEPH",  # IRNSS Ephemeris
    b"\x17\x00": "AGRIC",  # Position, velocity, serial number, heading, and baseline information
    b"\x18\x00": "PVTSLN",  # Position and Heading Information
    b"\x19\x00": "UNILOGLIST",  # Output Log List
    b"\x1a\x00": "BESTNAV",  # Best Position and Velocity
    b"\x1b\x00": "BESTNAVXYZ",  # Best Position and Velocity in ECEF
    b"\x1c\x00": "BESTNAVH",  # Best Position and Velocity (2nd Antenna)
    b"\x1d\x00": "BESTNAVXYZH",  # Best Position and Velocity in ECEF (2nd Antenna)
    b"\x1e\x00": "BESTSAT",  # Satellites Used in Position Solution
    b"\x1f\x00": "ADRNAV",  # RTK Position and Velocity
    b"\x20\x00": "ADRNAVH",  # RTK Position and Velocity (2nd Antenna)
    b"\x21\x00": "PPPNAV",  # Position and Velocity of PPP
    b"\x22\x00": "SPPNAV",  # Pseudorange Position and Velocity
    b"\x23\x00": "SPPNAVH",  # Pseudorange Position and Velocity (2nd Antenna)
    b"\x24\x00": "STADOP",  # DOP of BESTNAV
    b"\x25\x00": "STADOPH",  # DOP of BESTNAVH (2nd Antenna)
    b"\x26\x00": "ADRDOP",  # DOP of ADRNAV
    b"\x27\x00": "ADRDOPH",  # DOP of ADRNAVH (2nd Antenna)
    b"\x28\x00": "PPPDOP",  # DOP of PPPNAV
    b"\x29\x00": "SPPDOP",  # DOP of SPPNAV
    b"\x2a\x00": "SPPDOPH",  # DOP of SPPNAVH (2nd Antenna)
    b"\x2b\x00": "SATSINFO",  # Satellite Information
    b"\x2c\x00": "BASEPOS",  # Position of the Base Station
    b"\x2d\x00": "SATELLITE",  # Visible Satellites
    b"\x2e\x00": "SATECEF",  # Satellite Coordinates in ECEF
    b"\x2f\x00": "RECTIME",  # Time Information
    b"\x30\x00": "UNIHEADING",  # Heading Information
    b"\x31\x00": "UNIHEADING2",  # Multi-Rover Heading Information
    b"\x32\x00": "HEADINGSTATUS",  # Heading Status
    b"\x33\x00": "RTKSTATUS",  # RTK Solution Status
    b"\x34\x00": "AGNSSSTATUS",  # AGNSS Status
    b"\x35\x00": "RTCSTATUS",  # RTC Initialization Status
    b"\x36\x00": "JAMSTATUS",  # Jamming Detection
    b"\x37\x00": "FREQJAMSTATUS",  # Frequency Jamming Status
    b"\x38\x00": "RTCMSTATUS",  # RTCM Data Status
    b"\x39\x00": "HWSTATUS",  # Hardware Status
    b"\x3a\x00": "AGC",  # Automatic Gain Control
    b"\x3b\x00": "KSXT",  # Positioning and Heading Data Output
    b"\x3c\x00": "INFOPART1",  # Read user-defined information in PART1
    b"\x3d\x00": "INFOPART2",  # Read user-defined information in PART2
    b"\x3e\x00": "MSPOS",  # Best Position of Dual Antennas
    b"\x3f\x00": "TROPINFO",  # Zenith Tropospheric Delay
    b"\x40\x00": "PPPB2BINFO1",  # Information Type 1
    b"\x41\x00": "PPPB2BINFO2",  # Information Type 2
    b"\x42\x00": "PPPB2BINFO3",  # Information Type 3
    b"\x43\x00": "PPPB2BINFO4",  # Information Type 4
    b"\x44\x00": "PPPB2BINFO5",  # Information Type 5
    b"\x45\x00": "PPPB2BINFO6",  # Information Type 6
    b"\x46\x00": "PPPB2BINFO7",  # Information Type 7
    b"\x47\x00": "E6MASKBLOCK",  # Mask Block
    b"\x48\x00": "E6ORBITBLOCK",  # Orbit Corrections Block
    b"\x49\x00": "E6CLOCKFULLBLOCK",  # Clock Full-Set Corrections Block
    b"\x4a\x00": "E6CLOCKSUBBLOCK",  # Clock Subset Corrections Block
    b"\x4b\x00": "E6CBIASBLOCK",  # Code Biases Block
    b"\x4c\x00": "E6PBIASBLOCK",  # Phase Biases Block
    b"\x4d\x00": "BSLNENUHD2",  # Heading2 Baseline in ENU Coordinate System
    b"\x4e\x00": "BSLNXYZHD2",  # Heading2 Baseline in XYZ Coordinate System
    b"\x4f\x00": "DOPHD2",  # DOP of Heading2
    # TODO remove after Alpha..
    b"\x00\x12": "TEST12",
    b"\x00\x14": "TEST14",
}
