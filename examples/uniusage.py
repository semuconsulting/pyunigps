"""
uniusage.py

Illustrate basic usage of the pyunigps.UNIMessage and pyunigps.UNIReader classes.

Run from /examples folder

Created on 26 Jan 2026

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2025
:license: BSD 3-Clause
"""

import socket

from serial import Serial

from pyunigps import (
    ERR_IGNORE,
    ERR_LOG,
    ERR_RAISE,
    NMEA_PROTOCOL,
    RTCM3_PROTOCOL,
    UNI_PROTOCOL,
    VALCKSUM,
    UNIMessage,
    UNIReader,
)

# Processing serial stream containing UNI, NMEA and RTCM3 data:
TTYPORT = "/dev/ttyACM0"
with Serial(TTYPORT, 115200, timeout=3) as stream:
    unr = UNIReader(
        stream,
        protfilter=UNI_PROTOCOL | NMEA_PROTOCOL | RTCM3_PROTOCOL,
        quitonerror=ERR_LOG,
        validate=VALCKSUM,
        parsebitfield=True,
    )
    raw_data, parsed_data = unr.read()
    if parsed_data is not None:
        print(parsed_data)

# Processing binary file filtering on UNI data only:
INFILE = "pygpsdata_u980.log"
with open(INFILE, "rb") as stream:
    unr = UNIReader(
        stream, protfilter=UNI_PROTOCOL, validate=VALCKSUM, quitonerror=ERR_RAISE
    )
    for raw_data, parsed_data in unr:
        print(parsed_data)

# Processing socket stream containing UNI and NMEA data:
TCPADDR = "localhost"
TCPPORT = 5007
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
    stream.connect((TCPADDR, TCPPORT))
    unr = UNIReader(
        stream,
        protfilter=NMEA_PROTOCOL | UNI_PROTOCOL,
        validate=VALCKSUM,
        quitonerror=ERR_IGNORE,
    )
    for raw_data, parsed_data in unr:
        print(parsed_data)

# Create UNI VERSION message from keyword arguments
# (NB: Once created, UNIMessages are immutable):
msg = UNIMessage(
    msgid=17,
    wno=None,  # will default to current datetime
    tow=None,  # "
    device="M982",
    swversion="R4.10Build5251",
    authtype="HRPT00-S10C-P",
    psn="-",
    efuseid="ffff48ffff0fffff",
    comptime="2021/11/26",
)
print(msg)
