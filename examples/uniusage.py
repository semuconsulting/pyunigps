"""
uniusage.py

Illustrate basic usage of the pyunigps.UNIMessage and pyunigps.UNIReader classes.

Run from /examples folder

Created on 6 Oct 2025

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2025
:license: BSD 3-Clause
"""

from serial import Serial

from pyunigps import (
    ERR_LOG,
    GET,
    NMEA_PROTOCOL,
    POLL,
    UNI_PROTOCOL,
    RTCM3_PROTOCOL,
    SET,
    VALCKSUM,
    UNIMessage,
    UNIReader,
)
