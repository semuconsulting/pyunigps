"""
UNImessage.py

Main UNI Message Protocol Class.

Created on 26 Sep 2020

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2020
:license: BSD 3-Clause
"""

# pylint: disable=too-many-positional-arguments, too-many-locals, too-many-arguments, too-many-instance-attributes

import struct
from types import NoneType

from pyunigps.exceptions import UNIMessageError, UNITypeError
from pyunigps.unihelpers import (
    attsiz,
    bytes2val,
    calc_crc,
    escapeall,
    header2bytes,
    nomval,
    utc2wnotow,
    val2bytes,
)
from pyunigps.unitypes_core import (
    GET,
    POLL,
    SCALROUND,
    SET,
    UNI_HDR,
    UNI_MSGIDS,
)
from pyunigps.unitypes_get import UNI_PAYLOADS_GET
from pyunigps.unitypes_poll import UNI_PAYLOADS_POLL
from pyunigps.unitypes_set import UNI_PAYLOADS_SET


class UNIMessage:
    """UNI Message Class."""

    def __init__(
        self,
        msgid: int,
        length: int | NoneType = None,
        cpuidle: int = 0,
        timeref: int = 0,
        timestatus: int = 0,
        wno: int | NoneType = None,
        tow: int | NoneType = None,
        version: int = 0,
        leapsecond: int = 0,
        delay: int = 0,
        checksum: bytes | NoneType = None,
        msgmode: int = GET,
        parsebitfield: bool = True,
        **kwargs,
    ):
        """
        If no keyword parms are passed, the payload is taken to be empty.

        If 'payload' is passed as a keyword parm, this is taken to contain the complete
        payload as a sequence of bytes; any other keyword parms are ignored.

        Otherwise, any named attributes will be assigned the value given, all others will
        be assigned a nominal value according to type.

        :param msgid: msgid
        :param int | NoneType length: length (will be derived if None)
        :param int cpuidle: header cpuidle
        :param int timeref: header timeref
        :param int timestatus: header timestatus
        :param int | NoneType wno: header week number
        :param int | NoneType tow: header time of week
        :param int version: header version
        :param int leapsecond: header leapsecond
        :param int delay: header delay
        :param bytes | NoneType checksum: CRC (will be derived if None)
        :param int msgmode: message mode (0 = GET, 1 = SET, 2 = POLL)
        :param bool parsebitfield: 0 = parse as bytes, 1 = parse as individual bits
        :param kwargs: optional keywords representing payload attributes
        :raises: UNITypeError, UNIMessageError
        """

        # object is mutable during initialisation only
        super().__setattr__("_immutable", False)
        self.cpuidle = cpuidle
        self._length = length
        self._checksum = checksum  # bytes
        self._msgid = msgid
        self.cpuidle = cpuidle
        self.timeref = timeref
        self.timestatus = timestatus
        if wno is None or tow is None:  # default to now
            wno, tow = utc2wnotow()
        self.wno = wno
        self.tow = tow
        self.version = version
        self.leapsecond = leapsecond
        self.delay = delay
        self._mode = msgmode
        self._payload = b""
        self._parsebf = parsebitfield  # parsing bitfields Y/N?

        if msgmode not in (GET, SET, POLL):
            raise UNIMessageError(f"Invalid msgmode {msgmode} - must be 0, 1 or 2")

        self._do_attributes(**kwargs)

        self._immutable = True  # once initialised, object is immutable

    def _do_attributes(self, **kwargs):
        """
        Populate UNIMessage from named attribute keywords.
        Where a named attribute is absent, set to a nominal value (zeros or blanks).

        :param kwargs: optional payload key/value pairs
        :raises: UNITypeError

        """

        offset = 0  # payload offset in bytes
        index = []  # array of (nested) group indices

        try:
            if len(kwargs) == 0:  # if no kwargs, assume null payload
                self._payload = None
            else:
                self._payload = kwargs.get("payload", b"")
                pdict = self._get_dict(**kwargs)  # get appropriate payload dict
                for anam in pdict:  # process each attribute in dict
                    offset, index = self._set_attribute(
                        anam, pdict, offset, index, **kwargs
                    )
            self._do_len_checksum()

        except (
            AttributeError,
            struct.error,
            TypeError,
            ValueError,
        ) as err:
            raise UNITypeError(
                (
                    f"Incorrect type for attribute '{anam}' "
                    f"in {['GET', 'SET', 'POLL'][self._mode]} message class {self.identity}"
                )
            ) from err
        except (OverflowError,) as err:
            raise UNITypeError(
                (
                    f"Overflow error for attribute '{anam}' "
                    f"in {['GET', 'SET', 'POLL'][self._mode]} message class {self.identity}"
                )
            ) from err

    def _set_attribute(
        self, anam: str, pdict: dict, offset: int, index: list, **kwargs
    ) -> tuple:
        """
        Recursive routine to set individual or grouped payload attributes.

        :param str anam: attribute name
        :param dict pdict: dict representing payload definition
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (offset, index[])
        :rtype: tuple

        """

        adef = pdict[anam]  # get attribute definition
        if isinstance(
            adef, tuple
        ):  # repeating group of attributes or subdefined bitfield
            numr, _ = adef
            if numr[0] == "X":  # bitfield
                if self._parsebf:  # if we're parsing bitfields
                    offset, index = self._set_attribute_bitfield(
                        adef, offset, index, **kwargs
                    )
                else:  # treat bitfield as a single byte array
                    offset = self._set_attribute_single(
                        anam, numr, offset, index, **kwargs
                    )
            else:  # repeating group of attributes
                offset, index = self._set_attribute_group(adef, offset, index, **kwargs)
        else:  # single attribute
            offset = self._set_attribute_single(anam, adef, offset, index, **kwargs)

        return (offset, index)

    def _set_attribute_group(
        self, adef: tuple, offset: int, index: list, **kwargs
    ) -> tuple:
        """
        Process (nested) group of attributes.

        :param tuple adef: attribute definition - tuple of (num repeats, attribute dict)
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (offset, index[])
        :rtype: tuple

        """

        index.append(0)  # add a (nested) group index
        anam, gdict = adef  # attribute signifying group size, group dictionary
        # derive or retrieve number of items in group
        if isinstance(anam, int):  # fixed number of repeats
            gsiz = anam
        elif anam == "None":  # number of repeats 'variable by size'
            gsiz = self._calc_num_repeats(gdict, self._payload, offset, 0)
        else:  # number of repeats is defined in named attribute
            gsiz = getattr(self, anam)
        # recursively process each group attribute,
        # incrementing the payload offset and index as we go
        for i in range(gsiz):
            index[-1] = i + 1
            for key1 in gdict:
                offset, index = self._set_attribute(
                    key1, gdict, offset, index, **kwargs
                )

        index.pop()  # remove this (nested) group index

        return (offset, index)

    def _set_attribute_single(
        self, anam: str, adef: str | list, offset: int, index: list, **kwargs
    ) -> int:
        """
        Set individual attribute value, applying scaling where appropriate.

        :param str anam: attribute keyword
        :param str | list adef: attribute definition string e.g. 'U002'
           or, if scaled, list of [attribute type string, scaling factor float]
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: offset
        :rtype: int

        """
        # pylint: disable=no-member

        # if attribute is scaled
        ares = 1
        if isinstance(adef, list):
            ares = adef[1]  # attribute resolution (i.e. scaling factor)
            adef = adef[0]  # attribute definition

        # if attribute is part of a (nested) repeating group, suffix name with index
        anami = anam
        for i in index:  # one index for each nested level
            if i > 0:
                anami += f"_{i:02d}"

        # determine attribute size (bytes) - some attributes have
        # variable length, depending on
        # - multiple of value of preceding attribute
        # - payload length - offset
        asiz = attsiz(adef)

        # if payload keyword has been provided,
        # use the appropriate offset of the payload
        if "payload" in kwargs:
            valb = self._payload[offset : offset + asiz]
            if ares == 1:
                val = bytes2val(valb, adef)
            else:
                val = round(bytes2val(valb, adef) * ares, SCALROUND)
        else:
            # if individual keyword has been provided,
            # set to provided value, else set to
            # nominal value
            val = kwargs.get(anami, nomval(adef))
            if ares == 1:
                valb = val2bytes(val, adef)
            else:
                valb = val2bytes(int(val / ares), adef)
            self._payload += valb

        setattr(self, anami, val)

        return offset + asiz

    def _set_attribute_bitfield(
        self, atyp: str, offset: int, index: list, **kwargs
    ) -> tuple:
        """
        Parse bitfield attribute (type 'X').

        :param str atyp: attribute type e.g. 'X002'
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (offset, index[])
        :rtype: tuple

        """
        # pylint: disable=no-member

        btyp, bdict = atyp  # type of bitfield, bitfield dictionary
        bsiz = attsiz(btyp)  # size of bitfield in bytes
        bfoffset = 0

        # if payload keyword has been provided,
        # use the appropriate offset of the payload
        if "payload" in kwargs:
            bitfield = int.from_bytes(self._payload[offset : offset + bsiz], "little")
        else:
            bitfield = 0

        # process each flag in bitfield
        for key, keyt in bdict.items():
            bitfield, bfoffset = self._set_attribute_bits(
                bitfield, bfoffset, key, keyt, index, **kwargs
            )

        # update payload
        if "payload" not in kwargs:
            self._payload += bitfield.to_bytes(bsiz, "little")

        return (offset + bsiz, index)

    def _set_attribute_bits(
        self,
        bitfield: int,
        bfoffset: int,
        key: str,
        keyt: str,
        index: list,
        **kwargs,
    ) -> tuple:
        """
        Set individual bit flag from bitfield.

        :param int bitfield: bitfield
        :param int bfoffset: bitfield offset in bits
        :param str key: attribute key name
        :param str keyt: key type e.g. 'U001'
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (bitfield, bfoffset)
        :rtype: tuple

        """
        # pylint: disable=no-member

        # if attribute is part of a (nested) repeating group, suffix name with index
        keyr = key
        for i in index:  # one index for each nested level
            if i > 0:
                keyr += f"_{i:02d}"

        atts = attsiz(keyt)  # determine flag size in bits

        if "payload" in kwargs:
            val = (bitfield >> bfoffset) & ((1 << atts) - 1)
        else:
            val = kwargs.get(keyr, 0)
            bitfield = bitfield | (val << bfoffset)

        if key[0:8] != "reserved":  # don't bother to set reserved bits
            setattr(self, keyr, val)
        return (bitfield, bfoffset + atts)

    def _do_len_checksum(self):
        """
        Calculate and format payload length and checksum as bytes,
        if not passed as input arguments.
        """

        payload = b"" if self._payload is None else self._payload
        if self._length is None:
            self._length = len(payload)
        if self._checksum is None:
            self._checksum = calc_crc(
                UNI_HDR
                + header2bytes(
                    self._msgid,
                    self._length,
                    self.cpuidle,
                    self.timeref,
                    self.timestatus,
                    self.wno,
                    self.tow,
                    self.version,
                    self.leapsecond,
                    self.delay,
                )
                + payload
            )

    def _get_dict(self, **kwargs) -> dict:  # pylint: disable=unused-argument
        """
        Get payload dictionary corresponding to message mode (GET/SET/POLL)

        :param kwargs: optional payload key/value pairs
        :return: dictionary representing payload definition
        :rtype: dict

        """

        try:
            if self._mode == POLL:
                pdict = UNI_PAYLOADS_POLL[self.identity]
            elif self._mode == SET:
                pdict = UNI_PAYLOADS_SET[self.identity]
            else:
                # Unknown GET message, parsed to nominal definition
                if self.identity[-7:] == "NOMINAL":
                    pdict = {}
                else:
                    pdict = UNI_PAYLOADS_GET[self.identity]
            return pdict
        except KeyError as err:
            mode = ["GET", "SET", "POLL"][self._mode]
            raise UNIMessageError(
                f"Unknown message type {self._msgid}, mode {mode}"
            ) from err

    def _calc_num_repeats(
        self, attd: dict, payload: bytes, offset: int, offsetend: int = 0
    ) -> int:
        """
        Deduce number of items in 'variable by size' repeating group by
        dividing length of remaining payload by length of group.

        This is predicated on there being only one such repeating group
        per message payload, which is true for all currently supported types.

        :param dict attd: grouped attribute dictionary
        :param bytes payload : raw payload
        :param int offset: number of bytes in payload before repeating group
        :param int offsetend: number of bytes in payload after repeating group
        :return: number of repeats
        :rtype: int

        """

        lenpayload = len(payload) - offset - offsetend
        lengroup = 0
        for _, val in attd.items():
            if isinstance(val, tuple):
                val, _ = val
            lengroup += attsiz(val)
        return int(lenpayload / lengroup)

    def __str__(self) -> str:
        """
        Human readable representation.

        :return: human readable representation
        :rtype: str

        """

        umsg_name = self.identity
        if self.payload is None:
            return f"<UNI({umsg_name})>"
        if self.identity[-7:] == "NOMINAL":
            return f"<UNI({umsg_name}, payload={escapeall(self._payload)})>"

        stg = f"<UNI({umsg_name}, "
        for i, att in enumerate(self.__dict__):
            if att[0] != "_":  # only show public attributes
                val = self.__dict__[att]
                # escape all byte chars unless they're
                # intended to be character strings
                if isinstance(val, bytes):
                    val = escapeall(val)
                stg += att + "=" + str(val).strip(" ")
                if i < len(self.__dict__) - 1:
                    stg += ", "
        stg += ")>"

        return stg

    def __repr__(self) -> str:
        """
        Machine readable representation.

        eval(repr(obj)) = obj

        :return: machine readable representation
        :rtype: str

        """

        rep = (
            f"UNIMessage({self._msgid}, {self._length}, {self.cpuidle}, {self.timeref}, "
            f"{self.timestatus},{self.wno}, {self.tow}, {self.version}, {self.leapsecond}, "
            f"{self.delay}, {self.checksum}, {self._mode}, {self._parsebf}"
        )
        if self._payload is not None:
            rep += f", payload={self._payload})"
        return rep

    def __setattr__(self, name, value):
        """
        Override setattr to make object immutable after instantiation.

        :param str name: attribute name
        :param object value: attribute value
        :raises: UNIMessageError

        """

        if self._immutable:
            raise UNIMessageError(
                f"Object is immutable. Updates to {name} not permitted after initialisation."
            )

        super().__setattr__(name, value)

    def serialize(self) -> bytes:
        """
        Serialize message.

        :return: serialized output
        :rtype: bytes

        """

        hdr = header2bytes(
            self._msgid,
            self._length,
            self.cpuidle,
            self.timeref,
            self.timestatus,
            self.wno,
            self.tow,
            self.version,
            self.leapsecond,
            self.delay,
        )
        payloadb = b"" if self._payload is None else self._payload
        return UNI_HDR + hdr + payloadb + self._checksum

    @property
    def identity(self) -> str:
        """
        Returns message identity in plain text form.

        If the message is unrecognised, the message is parsed
        to a nominal payload definition UNI-NOMINAL and
        the term 'NOMINAL' is appended to the identity.

        :return: message identity e.g. 'OBSVMCMP'
        :rtype: str

        """

        try:
            umsg_name = UNI_MSGIDS[self._msgid]
        except KeyError:
            # unrecognised Unicore message, parsed to UNI-NOMINAL definition
            umsg_name = f"{int.from_bytes(self._msgid, 'little'):02x}-NOMINAL"
        return umsg_name

    @property
    def checksum(self) -> bytes:
        """
        CRC checksum getter.

        :return: CRC as bytes
        :rtype: bytes

        """

        return self._checksum

    @property
    def payload(self) -> bytes:
        """
        Payload getter - returns the raw payload bytes.

        :return: raw payload as bytes
        :rtype: bytes

        """

        return self._payload

    @property
    def msgmode(self) -> int:
        """
        Message mode getter.

        :return: msgmode as integer
        :rtype: int

        """

        return self._mode
