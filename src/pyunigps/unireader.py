"""
UNIReader class.

Reads and parses individual UNI messages from any viable
data stream which supports a read(n) -> bytes method.

UNI message bit format (little-endian):

+----------+---------+---------+---------+-----------+----------+---------+
|   sync   | cpuidle |  msgid  | length  | timeinfo  | payload  |   crc   |
+==========+=========+=========+=========+===========+==========+=========+
| 0xaa44b5 | 1 byte  | 2 bytes | 2 bytes | 16 bytes  | variable | 4 bytes |
+----------+---------+---------+---------+-----------+----------+---------+
|                  header = 24 bytes                 |          |         |
+----------+---------+---------+---------+-----------+----------+---------+

timeinfo:

+---------+----------+---------+---------+---------+----------+---------+---------+
| timeref | timestat |   wno   |   tow   | version | reserved | leapsec |  delay  |
+=========+==========+=========+=========+=========+==========+=========+=========+
| 1 byte  |  1 byte  | 2 bytes | 4 bytes | 4 bytes |  1 byte  | 1 byte  | 2 bytes |
+---------+----------+---------+---------+---------+----------+---------+---------+

Returns both the raw binary data (as bytes) and the parsed data
(as an UNIMessage object).

- 'protfilter' governs which protocols (NMEA, UNI or RTCM3) are processed
- 'quitonerror' governs how errors are handled
- 'parsing' governs whether messages are fully parsed

Created on 26 Jan 2026

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2020
:license: BSD 3-Clause
"""

# pylint: disable=too-many-positional-arguments

from logging import getLogger
from socket import socket

import pynmeagps.exceptions as nme
import pyrtcm.exceptions as rte
from pynmeagps import NMEA_HDR, NMEAReader, SocketWrapper
from pyrtcm import RTCMReader

from pyunigps.exceptions import (
    UNIMessageError,
    UNIParseError,
    UNIStreamError,
    UNITypeError,
)
from pyunigps.unihelpers import (
    bytes2val,
    calc_crc,
    escapeall,
    val2bytes,
)
from pyunigps.unimessage import UNIMessage
from pyunigps.unitypes_core import (
    ERR_LOG,
    ERR_RAISE,
    GET,
    NMEA_PROTOCOL,
    POLL,
    RTCM3_PROTOCOL,
    SET,
    SETPOLL,
    U1,
    U2,
    U4,
    UNI_HDR,
    UNI_PROTOCOL,
    VALCKSUM,
)


class UNIReader:
    """
    UNIReader class.
    """

    def __init__(
        self,
        datastream,
        msgmode: int = GET,
        validate: int = VALCKSUM,
        protfilter: int = NMEA_PROTOCOL | UNI_PROTOCOL | RTCM3_PROTOCOL,
        quitonerror: int = ERR_LOG,
        parsebitfield: bool = True,
        bufsize: int = 4096,
        parsing: bool = True,
        errorhandler: object = None,
    ):
        """Constructor.

        :param datastream stream: input data stream
        :param int msgmode: 0=GET, 1=SET, 2=POLL, 3=SETPOLL (0)
        :param int validate: VALCKSUM (1) = Validate checksum,
            VALNONE (0) = ignore invalid checksum (1)
        :param int protfilter: NMEA_PROTOCOL (1), UNI_PROTOCOL (2), RTCM3_PROTOCOL (4),
            Can be OR'd (7)
        :param int quitonerror: ERR_IGNORE (0) = ignore errors,  ERR_LOG (1) = log continue,
            ERR_RAISE (2) = (re)raise (1)
        :param bool parsebitfield: 1 = parse bitfields, 0 = leave as bytes (1)
        :param int bufsize: socket recv buffer size (4096)
        :param bool parsing: True = parse data, False = don't parse data (output raw only) (True)
        :param object errorhandler: error handling object or function (None)
        :raises: UNIStreamError (if mode is invalid)
        """
        # pylint: disable=too-many-arguments

        if isinstance(datastream, socket):
            self._stream = SocketWrapper(datastream, bufsize=bufsize)
        else:
            self._stream = datastream
        self._protfilter = protfilter
        self._quitonerror = quitonerror
        self._errorhandler = errorhandler
        self._validate = validate
        self._parsebf = parsebitfield
        self._msgmode = msgmode
        self._parsing = parsing
        self._logger = getLogger(__name__)

        if self._msgmode not in (GET, SET, POLL, SETPOLL):
            raise UNIStreamError(
                f"Invalid stream mode {self._msgmode} - must be 0, 1, 2 or 3"
            )

    def __iter__(self):
        """Iterator."""

        return self

    def __next__(self) -> tuple:
        """
        Return next item in iteration.

        :return: tuple of (raw_data as bytes, parsed_data as UNIMessage)
        :rtype: tuple
        :raises: StopIteration

        """

        raw_data, parsed_data = self.read()
        if raw_data is None and parsed_data is None:
            raise StopIteration
        return (raw_data, parsed_data)

    def read(self) -> tuple:
        """
        Read a single UNI message from the stream buffer
        and return both raw and parsed data.

        'quitonerror' determines whether to raise, log or ignore parsing errors.

        :return: tuple of (raw_data as bytes, parsed_data as UNIMessage)
        :rtype: tuple
        :raises: Exception (if invalid or unrecognised protocol in data stream)
        """

        parsing = True
        while parsing:  # loop until end of valid message or EOF
            try:

                raw_data = None
                parsed_data = None
                byte1 = self._read_bytes(1)  # read the first byte
                # if not UNI, NMEA or RTCM3, discard and continue
                if byte1 not in (b"\xaa", b"\x24", b"\xd3"):
                    continue
                byte2 = self._read_bytes(1)
                bytehdr = byte1 + byte2
                if bytehdr == UNI_HDR[0:2]:
                    byte3 = self._read_bytes(1)
                    bytehdr += byte3
                    # if it's a UNI message (b'\xaa\x44\b5')
                    if bytehdr != UNI_HDR:
                        continue
                    raw_data, parsed_data = self._parse_uni(bytehdr)
                    # if protocol filter passes UNI, return message,
                    # otherwise discard and continue
                    if self._protfilter & UNI_PROTOCOL:
                        parsing = False
                    else:
                        continue
                # if it's an NMEA message (b'\x24\x..)
                elif bytehdr in NMEA_HDR:
                    raw_data, parsed_data = self._parse_nmea(bytehdr)
                    # if protocol filter passes NMEA, return message,
                    # otherwise discard and continue
                    if self._protfilter & NMEA_PROTOCOL:
                        parsing = False
                    else:
                        continue
                # if it's a RTCM3 message
                # (byte1 = 0xd3; byte2 = 0b000000**)
                elif byte1 == b"\xd3" and (byte2[0] & ~0x03) == 0:
                    raw_data, parsed_data = self._parse_rtcm3(bytehdr)
                    # if protocol filter passes RTCM, return message,
                    # otherwise discard and continue
                    if self._protfilter & RTCM3_PROTOCOL:
                        parsing = False
                    else:
                        continue
                # unrecognised protocol header
                else:
                    raise UNIParseError(f"Unknown protocol header {bytehdr}.")

            except EOFError:
                return (None, None)
            except (
                UNIMessageError,
                UNITypeError,
                UNIParseError,
                UNIStreamError,
                nme.NMEAMessageError,
                nme.NMEATypeError,
                nme.NMEAParseError,
                nme.NMEAStreamError,
                rte.RTCMMessageError,
                rte.RTCMParseError,
                rte.RTCMStreamError,
                rte.RTCMTypeError,
            ) as err:
                if self._quitonerror:
                    self._do_error(err)
                continue

        return (raw_data, parsed_data)

    def _parse_uni(self, hdr: bytes) -> tuple:
        """
        Parse remainder of UNI message.

        :param bytes hdr: UNI header (b'\\xaa\\x44\\xb5')
        :return: tuple of (raw_data as bytes, parsed_data as UNIMessage or None)
        :rtype: tuple
        """

        # read the rest of the UNI message from the buffer
        byten = self._read_bytes(21)
        cpuidle = byten[0:1]
        msgid = byten[1:3]
        lenb = byten[3:5]
        timeinfo = byten[5:21]
        leni = int.from_bytes(lenb, "little", signed=False)
        byten = self._read_bytes(leni + 4)
        plb = byten[0:leni]
        crc = byten[leni : leni + 4]
        raw_data = hdr + cpuidle + msgid + lenb + timeinfo + plb + crc
        # only parse if we need to (filter passes UNI)
        if (self._protfilter & UNI_PROTOCOL) and self._parsing:
            parsed_data = self.parse(
                raw_data,
                msgmode=self._msgmode,
                validate=self._validate,
                parsebitfield=self._parsebf,
            )
        else:
            parsed_data = None
        return (raw_data, parsed_data)

    def _parse_nmea(self, hdr: bytes) -> tuple:
        """
        Parse remainder of NMEA message (using pynmeagps library).

        :param bytes hdr: NMEA header (b'\\x24\\x..')
        :return: tuple of (raw_data as bytes, parsed_data as NMEAMessage or None)
        :rtype: tuple
        """

        # read the rest of the NMEA message from the buffer
        byten = self._read_line()  # NMEA protocol is CRLF-terminated
        raw_data = hdr + byten
        # only parse if we need to (filter passes NMEA)
        if (self._protfilter & NMEA_PROTOCOL) and self._parsing:
            # invoke pynmeagps parser
            parsed_data = NMEAReader.parse(
                raw_data,
                validate=self._validate,
                msgmode=self._msgmode,
            )
        else:
            parsed_data = None
        return (raw_data, parsed_data)

    def _parse_rtcm3(self, hdr: bytes) -> tuple:
        """
        Parse any RTCM3 data in the stream (using pyrtcm library).

        :param bytes hdr: first 2 bytes of RTCM3 header
        :return: tuple of (raw_data as bytes, parsed_stub as RTCMMessage)
        :rtype: tuple
        """

        hdr3 = self._read_bytes(1)
        size = hdr3[0] | (hdr[1] << 8)
        payload = self._read_bytes(size)
        crc = self._read_bytes(3)
        raw_data = hdr + hdr3 + payload + crc
        # only parse if we need to (filter passes RTCM)
        if (self._protfilter & RTCM3_PROTOCOL) and self._parsing:
            # invoke pyrtcm parser
            parsed_data = RTCMReader.parse(
                raw_data,
                validate=self._validate,
                labelmsm=1,
            )
        else:
            parsed_data = None
        return (raw_data, parsed_data)

    def _read_bytes(self, size: int) -> bytes:
        """
        Read a specified number of bytes from stream.

        :param int size: number of bytes to read
        :return: bytes
        :rtype: bytes
        :raises: UNIStreamError if stream ends prematurely
        """

        data = self._stream.read(size)
        if len(data) == 0:  # EOF
            raise EOFError()
        if 0 < len(data) < size:  # truncated stream
            raise UNIStreamError(
                "Serial stream terminated unexpectedly. "
                f"{size} bytes requested, {len(data)} bytes returned."
            )
        return data

    def _read_line(self) -> bytes:
        """
        Read bytes until LF (0x0a) terminator.

        :return: bytes
        :rtype: bytes
        :raises: UNIStreamError if stream ends prematurely
        """

        data = self._stream.readline()  # NMEA protocol is CRLF-terminated
        if len(data) == 0:
            raise EOFError()  # pragma: no cover
        if data[-1:] != b"\x0a":  # truncated stream
            raise UNIStreamError(
                "Serial stream terminated unexpectedly. "
                f"Line requested, {len(data)} bytes returned."
            )
        return data

    def _do_error(self, err: Exception):
        """
        Handle error.

        :param Exception err: error
        :raises: Exception if quitonerror = ERR_RAISE (2)
        """

        if self._quitonerror == ERR_RAISE:
            raise err from err
        if self._quitonerror == ERR_LOG:
            # pass to error handler if there is one
            # else just log
            if self._errorhandler is None:
                self._logger.error(err)
            else:
                self._errorhandler(err)

    @property
    def datastream(self) -> object:
        """
        Getter for stream.

        :return: data stream
        :rtype: object
        """

        return self._stream

    @staticmethod
    def parse(
        message: bytes,
        msgmode: int = GET,
        validate: int = VALCKSUM,
        parsebitfield: bool = True,
    ) -> object:
        """
        Parse UNI byte stream to UNIMessage object.

        :param bytes message: binary message to parse
        :param int msgmode: GET (0), SET (1), POLL (2) (0)
        :param int validate: VALCKSUM (1) = Validate checksum,
            VALNONE (0) = ignore invalid checksum (1)
        :param bool parsebitfield: 1 = parse bitfields, 0 = leave as bytes (1)
        :return: UNIMessage object
        :rtype: UNIMessage
        :raises: Exception (if data stream contains invalid data or unknown message type)
        """

        if msgmode not in (GET, SET, POLL, SETPOLL):
            raise UNIParseError(
                f"Invalid message mode {msgmode} - must be 0, 1, 2 or 3"
            )

        lenm = len(message)
        hdr = message[0:3]
        cpuidleb = message[3:4]
        cpuidle = bytes2val(cpuidleb, U1)
        msgidb = message[4:6]
        msgid = bytes2val(msgidb, U2)
        lenb = message[6:8]
        length = bytes2val(lenb, U2)
        timeref = bytes2val(message[8:9], U1)
        timestatus = bytes2val(message[9:10], U1)
        wno = bytes2val(message[10:12], U2)
        tow = bytes2val(message[12:16], U4)
        version = bytes2val(message[16:20], U4)
        leapsecond = bytes2val(message[21:22], U1)
        delay = bytes2val(message[22:24], U1)
        crcb = message[lenm - 4 : lenm]

        if lenb == b"\x00\x00\x00\x00":
            payload = None
            lenp = 0
        else:
            payload = message[24 : lenm - 4]
            lenp = len(payload)

        if payload is None:
            crc = calc_crc(message[0:24])
        else:
            crc = calc_crc(message[0:24] + payload)

        if validate & VALCKSUM:
            if hdr != UNI_HDR:
                raise UNIParseError(
                    (
                        f"Invalid message header {escapeall(hdr)}"
                        f" - should be {escapeall(UNI_HDR)}"
                    )
                )
            if lenp != length:
                raise UNIParseError(
                    (
                        f"Invalid payload length {escapeall(lenb)}"
                        f" - should be {val2bytes(lenp, U2)}"
                    )
                )
            if crc != crcb:
                raise UNIParseError(
                    (
                        f"Message checksum {escapeall(crcb)}"
                        f" invalid - should be {escapeall(crc)}"
                    )
                )
        parsed_data = UNIMessage(
            msgid=msgid,
            length=length,
            cpuidle=cpuidle,
            timeref=timeref,
            timestatus=timestatus,
            wno=wno,
            tow=tow,
            version=version,
            leapsecond=leapsecond,
            delay=delay,
            checksum=crcb,
            msgmode=msgmode,
            parsebitfield=parsebitfield,
            payload=payload,
        )
        return parsed_data
