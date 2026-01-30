"""
Collection of UNI helper methods which can be used
outside the UNIMessage or UNIReader classes.

Created on 6 Oct 2025

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2020
:license: BSD 3-Clause
"""

import struct
from datetime import datetime, timezone
from types import NoneType
from typing import Any

import pyunigps.exceptions as qge
from pyunigps.unitypes_core import ATTTYPE, U4

# base epoch for wno and tow
GPSEPOCH0 = datetime(1980, 1, 6, tzinfo=timezone.utc)
# CRC table for calculation in calc_crc
CRCTABLE = [
    0x00000000,
    0x77073096,
    0xEE0E612C,
    0x990951BA,
    0x076DC419,
    0x706AF48F,
    0xE963A535,
    0x9E6495A3,
    0x0EDB8832,
    0x79DCB8A4,
    0xE0D5E91E,
    0x97D2D988,
    0x09B64C2B,
    0x7EB17CBD,
    0xE7B82D07,
    0x90BF1D91,
    0x1DB71064,
    0x6AB020F2,
    0xF3B97148,
    0x84BE41DE,
    0x1ADAD47D,
    0x6DDDE4EB,
    0xF4D4B551,
    0x83D385C7,
    0x136C9856,
    0x646BA8C0,
    0xFD62F97A,
    0x8A65C9EC,
    0x14015C4F,
    0x63066CD9,
    0xFA0F3D63,
    0x8D080DF5,
    0x3B6E20C8,
    0x4C69105E,
    0xD56041E4,
    0xA2677172,
    0x3C03E4D1,
    0x4B04D447,
    0xD20D85FD,
    0xA50AB56B,
    0x35B5A8FA,
    0x42B2986C,
    0xDBBBC9D6,
    0xACBCF940,
    0x32D86CE3,
    0x45DF5C75,
    0xDCD60DCF,
    0xABD13D59,
    0x26D930AC,
    0x51DE003A,
    0xC8D75180,
    0xBFD06116,
    0x21B4F4B5,
    0x56B3C423,
    0xCFBA9599,
    0xB8BDA50F,
    0x2802B89E,
    0x5F058808,
    0xC60CD9B2,
    0xB10BE924,
    0x2F6F7C87,
    0x58684C11,
    0xC1611DAB,
    0xB6662D3D,
    0x76DC4190,
    0x01DB7106,
    0x98D220BC,
    0xEFD5102A,
    0x71B18589,
    0x06B6B51F,
    0x9FBFE4A5,
    0xE8B8D433,
    0x7807C9A2,
    0x0F00F934,
    0x9609A88E,
    0xE10E9818,
    0x7F6A0DBB,
    0x086D3D2D,
    0x91646C97,
    0xE6635C01,
    0x6B6B51F4,
    0x1C6C6162,
    0x856530D8,
    0xF262004E,
    0x6C0695ED,
    0x1B01A57B,
    0x8208F4C1,
    0xF50FC457,
    0x65B0D9C6,
    0x12B7E950,
    0x8BBEB8EA,
    0xFCB9887C,
    0x62DD1DDF,
    0x15DA2D49,
    0x8CD37CF3,
    0xFBD44C65,
    0x4DB26158,
    0x3AB551CE,
    0xA3BC0074,
    0xD4BB30E2,
    0x4ADFA541,
    0x3DD895D7,
    0xA4D1C46D,
    0xD3D6F4FB,
    0x4369E96A,
    0x346ED9FC,
    0xAD678846,
    0xDA60B8D0,
    0x44042D73,
    0x33031DE5,
    0xAA0A4C5F,
    0xDD0D7CC9,
    0x5005713C,
    0x270241AA,
    0xBE0B1010,
    0xC90C2086,
    0x5768B525,
    0x206F85B3,
    0xB966D409,
    0xCE61E49F,
    0x5EDEF90E,
    0x29D9C998,
    0xB0D09822,
    0xC7D7A8B4,
    0x59B33D17,
    0x2EB40D81,
    0xB7BD5C3B,
    0xC0BA6CAD,
    0xEDB88320,
    0x9ABFB3B6,
    0x03B6E20C,
    0x74B1D29A,
    0xEAD54739,
    0x9DD277AF,
    0x04DB2615,
    0x73DC1683,
    0xE3630B12,
    0x94643B84,
    0x0D6D6A3E,
    0x7A6A5AA8,
    0xE40ECF0B,
    0x9309FF9D,
    0x0A00AE27,
    0x7D079EB1,
    0xF00F9344,
    0x8708A3D2,
    0x1E01F268,
    0x6906C2FE,
    0xF762575D,
    0x806567CB,
    0x196C3671,
    0x6E6B06E7,
    0xFED41B76,
    0x89D32BE0,
    0x10DA7A5A,
    0x67DD4ACC,
    0xF9B9DF6F,
    0x8EBEEFF9,
    0x17B7BE43,
    0x60B08ED5,
    0xD6D6A3E8,
    0xA1D1937E,
    0x38D8C2C4,
    0x4FDFF252,
    0xD1BB67F1,
    0xA6BC5767,
    0x3FB506DD,
    0x48B2364B,
    0xD80D2BDA,
    0xAF0A1B4C,
    0x36034AF6,
    0x41047A60,
    0xDF60EFC3,
    0xA867DF55,
    0x316E8EEF,
    0x4669BE79,
    0xCB61B38C,
    0xBC66831A,
    0x256FD2A0,
    0x5268E236,
    0xCC0C7795,
    0xBB0B4703,
    0x220216B9,
    0x5505262F,
    0xC5BA3BBE,
    0xB2BD0B28,
    0x2BB45A92,
    0x5CB36A04,
    0xC2D7FFA7,
    0xB5D0CF31,
    0x2CD99E8B,
    0x5BDEAE1D,
    0x9B64C2B0,
    0xEC63F226,
    0x756AA39C,
    0x026D930A,
    0x9C0906A9,
    0xEB0E363F,
    0x72076785,
    0x05005713,
    0x95BF4A82,
    0xE2B87A14,
    0x7BB12BAE,
    0x0CB61B38,
    0x92D28E9B,
    0xE5D5BE0D,
    0x7CDCEFB7,
    0x0BDBDF21,
    0x86D3D2D4,
    0xF1D4E242,
    0x68DDB3F8,
    0x1FDA836E,
    0x81BE16CD,
    0xF6B9265B,
    0x6FB077E1,
    0x18B74777,
    0x88085AE6,
    0xFF0F6A70,
    0x66063BCA,
    0x11010B5C,
    0x8F659EFF,
    0xF862AE69,
    0x616BFFD3,
    0x166CCF45,
    0xA00AE278,
    0xD70DD2EE,
    0x4E048354,
    0x3903B3C2,
    0xA7672661,
    0xD06016F7,
    0x4969474D,
    0x3E6E77DB,
    0xAED16A4A,
    0xD9D65ADC,
    0x40DF0B66,
    0x37D83BF0,
    0xA9BCAE53,
    0xDEBB9EC5,
    0x47B2CF7F,
    0x30B5FFE9,
    0xBDBDF21C,
    0xCABAC28A,
    0x53B39330,
    0x24B4A3A6,
    0xBAD03605,
    0xCDD70693,
    0x54DE5729,
    0x23D967BF,
    0xB3667A2E,
    0xC4614AB8,
    0x5D681B02,
    0x2A6F2B94,
    0xB40BBE37,
    0xC30C8EA1,
    0x5A05DF1B,
    0x2D02EF8D,
]


def att2idx(att: str) -> int | tuple[int]:
    """
    Get integer indices corresponding to grouped attribute.

    e.g. svid_06 -> 6; gnssId_103 -> 103, gsid_03_04 -> (3,4), tow -> 0

    :param str att: grouped attribute name e.g. svid_01
    :return: indices as integer(s), or 0 if not grouped
    :rtype: int | tuple[int]
    """

    try:
        att = att.split("_")
        ln = len(att)
        if ln == 2:  # one group level
            return int(att[1])
        if ln > 2:  # nested group level(s)
            return tuple(int(att[i]) for i in range(1, ln))
        return 0  # not grouped
    except ValueError:
        return 0


def att2name(att: str) -> str:
    """
    Get name of grouped attribute.

    e.g. svid_06 -> svid; gnssId_103 -> gnssId, tow -> tow

    :param str att: grouped attribute name e.g. svid_01
    :return: name without index e.g. svid
    :rtype: str
    """

    return att.split("_")[0]


def attsiz(att: str) -> int:
    """
    Helper function to return attribute size in bytes.

    :param str: attribute type e.g. 'U002'
    :return: size of attribute in bytes, or -1 if variable length
    :rtype: int

    """

    try:
        return int(att[1:4])
    except ValueError:
        return -1


def atttyp(att: str) -> str:
    """
    Helper function to return attribute type as string.

    :param str: attribute type e.g. 'U002'
    :return: type of attribute as string e.g. 'U'
    :rtype: str

    """

    return att[0:1]


def bytes2val(valb: bytes, att: str) -> Any:
    """
    Convert bytes to value for given UNI attribute type.

    :param bytes valb: attribute value in byte format e.g. b'\\\\x19\\\\x00\\\\x00\\\\x00'
    :param str att: attribute type e.g. 'U004'
    :return: attribute value as int, float, str or bytes
    :rtype: Any
    :raises: UNITypeError

    """

    if atttyp(att) == "X":  # bytes
        val = valb
    elif atttyp(att) == "C":  # string
        val = valb.decode("utf-8", errors="backslashreplace")
    elif atttyp(att) in ("S", "U"):  # integer
        val = int.from_bytes(valb, byteorder="little", signed=atttyp(att) == "S")
    elif atttyp(att) == "R":  # floating point
        val = struct.unpack("<f" if attsiz(att) == 4 else "<d", valb)[0]
    else:
        raise qge.UNITypeError(f"Unknown attribute type {att}")
    return val


def calc_crc(message: bytes) -> bytes:
    """
    Perform CRC32 cyclic redundancy check.

    :param bytes message: message
    :return: CRC as bytes
    :rtype: bytes

    """

    size = len(message)
    crc = 0
    for i in range(size):
        crc = CRCTABLE[(crc ^ message[i]) & 0xFF] ^ (crc >> 8)
    return val2bytes(crc, U4)


def escapeall(val: bytes) -> str:
    """
    Escape all byte characters e.g. b'\\\\x73' rather than b`s`

    :param bytes val: bytes
    :return: string of escaped bytes
    :rtype: str
    """

    return "b'{}'".format("".join(f"\\x{b:02x}" for b in val))


def get_bits(bitfield: bytes, bitmask: int) -> int:
    """
    Get integer value of specified (masked) bit(s) in a UNI bitfield (attribute type 'X')

    e.g. to get value of bits 6,7 in bitfield b'\\\\x89' (binary 0b10001001)::

        get_bits(b'\\x89', 0b11000000) = get_bits(b'\\x89', 192) = 2

    :param bytes bitfield: bitfield byte(s)
    :param int bitmask: bitmask as integer (= Σ(2**n), where n is the number of the bit)
    :return: value of masked bit(s)
    :rtype: int
    """

    i = 0
    val = int(bitfield.hex(), 16)
    while bitmask & 1 == 0:
        bitmask = bitmask >> 1
        i += 1
    return val >> i & bitmask


def header2bytes(
    msgid: int,
    length: int,
    cpuidle: int = 0,
    timeref: int = 1,
    timestatus: int = 0,
    wno: int | NoneType = None,
    tow: int | NoneType = None,
    version: int = 0,
    leapsecond: int = 0,
    delay: int = 0,
) -> bytes:
    """
    Convert individual values to header structure
    (excluding 3 fixed sync bytes).

    :param int msgid: msgid
    :param int length: payload length
    :param int cpuidle: cpuidle
    :param int timeref: time reference (GPS/BDS)
    :param int timestatus: timestatus
    :param int | NoneType wno: week no (defaults to now if None)
    :param int | NoneType tow: time of week (defaults to now if None)
    :param int version: message version
    :param int leapsecond: leap second
    :param int delay: delay in ms
    :return: header as bytes
    :rtype: bytes
    """

    if wno is None or tow is None:
        wno, tow = utc2wnotow()
    return struct.pack(
        "<BHHBBHLLBBH",
        cpuidle,
        msgid,
        length,
        timeref,
        timestatus,
        wno,
        tow,
        version,
        0,  # reserved
        leapsecond,
        delay,
    )


def header2vals(header: bytes) -> tuple:
    """
    Convert header bytes (excluding 3 fixed sync bytes)
    into individual values.

    :param bytes header: header bytes
    :return: tuple of
      (cpuidle, msgid, length, timeref, timestatus, wno,
      tow, version, reserved, leapsecond, delay)
    """

    return struct.unpack("<BHHBBHLLBBH", header)


def isvalid_checksum(message: bytes) -> bool:
    """
    Validate message checksum.

    :param bytes message: message including header and checksum bytes
    :return: checksum valid flag
    :rtype: bool

    """

    lenm = len(message)
    ckm = message[lenm - 4 : lenm]
    return ckm == calc_crc(message[: lenm - 4])


def key_from_val(dictionary: dict, value) -> str:
    """
    Helper method - get dictionary key corresponding to (unique) value.

    :param dict dictionary: dictionary
    :param object value: unique dictionary value
    :return: dictionary key
    :rtype: str
    :raises: KeyError: if no key found for value

    """

    val = None
    for key, val in dictionary.items():
        if val == value:
            return key
    raise KeyError(f"No key found for value {value}")


def nomval(att: str) -> Any:
    """
    Get nominal value for given UNI attribute type.

    :param str att: attribute type e.g. 'U004'
    :return: attribute value as int, float, str or bytes
    :rtype: Any
    :raises: UNITypeError

    """

    if atttyp(att) == "X":
        val = b"\x00" * attsiz(att)
    elif atttyp(att) == "C":
        val = " " * attsiz(att)
    elif atttyp(att) == "R":
        val = 0.0
    elif atttyp(att) in ("S", "U"):
        val = 0
    else:
        raise qge.UNITypeError(f"Unknown attribute type {att}")
    return val


def utc2wnotow(utc: datetime | NoneType = None) -> tuple[int, int]:
    """
    Get GPS Week number (wno) and Time of Week (tow)
    in milliseconds for given utc datetime.

    GPS Epoch 0 = 6th Jan 1980

    :param datetime | NoneType utc: utc datetime (defaults to now if None)
    :return: wno, tow
    :rtype: tuple[int,int]
    """

    if utc is None:
        utc = datetime.now(tz=timezone.utc)
    ts = (utc - GPSEPOCH0).total_seconds() * 1000
    wno = int((utc - GPSEPOCH0).days / 7)
    tow = int(ts - wno * 604800000)
    return wno, tow


def val2bytes(val: Any, att: str) -> bytes:
    """
    Convert value to bytes for given UNI attribute type.

    :param Any val: attribute value e.g. 25
    :param str att: attribute type e.g. 'U004'
    :return: attribute value as bytes
    :rtype: bytes
    :raises: UNITypeError

    """

    try:
        if not isinstance(val, ATTTYPE[atttyp(att)]):
            raise TypeError(
                f"Attribute type {att} value {val} must be {ATTTYPE[atttyp(att)]}, not {type(val)}"
            )
    except KeyError as err:
        raise qge.UNITypeError(f"Unknown attribute type {att}") from err

    valb = val
    if atttyp(att) == "X":  # byte
        valb = val
    elif atttyp(att) == "C":  # string
        v = val.encode("utf-8", errors="backslashreplace")
        valb = v + b"\x20" * (attsiz(att) - len(v))  # right pad with spaces
    elif atttyp(att) in ("S", "U"):  # integer
        valb = val.to_bytes(attsiz(att), byteorder="little", signed=atttyp(att) == "S")
    elif atttyp(att) == "R":  # floating point
        valb = struct.pack("<f" if attsiz(att) == 4 else "<d", float(val))
    return valb
