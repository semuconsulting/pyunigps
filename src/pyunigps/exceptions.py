"""
UNI Custom Exception Types.

Created on 6 Oct 2025

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2020
:license: BSD 3-Clause
"""

from pynmeagps import NMEAMessageError, NMEAParseError, NMEAStreamError, NMEATypeError
from pyrtcm import RTCMMessageError, RTCMParseError, RTCMStreamError, RTCMTypeError


class ParameterError(Exception):
    """Parameter Error Class."""


class GNSSStreamError(Exception):
    """Generic Stream Error Class."""


class UNIParseError(Exception):
    """
    UNI Parsing error.
    """


class UNIStreamError(Exception):
    """
    UNI Streaming error.
    """


class UNIMessageError(Exception):
    """
    UNI Undefined message class/id.
    Essentially a prompt to add missing payload types to UNI_PAYLOADS.
    """


class UNITypeError(Exception):
    """
    UNI Undefined payload attribute type.
    Essentially a prompt to fix incorrect payload definitions to UNI_PAYLOADS.
    """


GNSSERRORS = (
    UNIMessageError,
    UNITypeError,
    UNIParseError,
    UNIStreamError,
    NMEAMessageError,
    NMEATypeError,
    NMEAParseError,
    NMEAStreamError,
    RTCMMessageError,
    RTCMParseError,
    RTCMStreamError,
    RTCMTypeError,
)
