"""
UNImessage.py

Main UNI Message Protocol Class.

Created on 26 Sep 2020

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2020
:license: BSD 3-Clause
"""

# pylint: disable=too-many-positional-arguments, too-many-locals, too-many-arguments, too-many-instance-attributes

from types import NoneType

from pyunigps.exceptions import UNIMessageError
from pyunigps.unihelpers import (
    attsiz,
    bytes2val,
    calc_crc,
    escapeall,
    header2bytes,
    msgname2id,
    nomval,
    utc2wnotow,
    val2bytes,
)
from pyunigps.unitypes_core import (
    FREQNO,
    GET,
    POLL,
    SCALROUND,
    SET,
    U1,
    UNI_HDR,
    UNI_MSGIDS,
)
from pyunigps.unitypes_decodes import PSRSTD
from pyunigps.unitypes_get import UNI_PAYLOADS_GET
from pyunigps.unitypes_poll import UNI_PAYLOADS_POLL
from pyunigps.unitypes_set import UNI_PAYLOADS_SET


class UNIMessage:
    """UNI Message Class."""

    def __init__(
        self,
        msgid: int | str,
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

        If the wno or tow arguments are `None`, wno, tow and leapsecond will default to the
        current datetime and leapsecond offset.

        Otherwise, any named attributes will be assigned the value given, all others will
        be assigned a nominal value according to type.

        :param int | str msgid: message id or message name
        :param int | NoneType length: length (will be derived if None)
        :param int cpuidle: header cpuidle
        :param int timeref: header timeref
        :param int timestatus: header timestatus
        :param int | NoneType wno: header week number (defaults to now if None)
        :param int | NoneType tow: header time of week (defaults to now if None)
        :param int version: header version
        :param int leapsecond: header leapsecond
        :param int delay: header delay
        :param bytes | NoneType checksum: CRC (will be derived if None)
        :param int msgmode: message mode (0 = GET, 1 = SET, 2 = POLL)
        :param bool parsebitfield: 0 = parse as bytes, 1 = parse as individual bits
        :param kwargs: optional keywords representing payload attributes
        :raises: UNITypeError, UNIMessageError
        """

        if msgmode not in (GET, SET, POLL):
            raise UNIMessageError(f"Invalid msgmode {msgmode} - must be 0, 1 or 2")

        # object is mutable during initialisation only
        super().__setattr__("_immutable", False)
        self.cpuidle = cpuidle
        self._length = length
        self._checksum = checksum  # bytes
        if isinstance(msgid, str):  # if msgname, convert to msgid
            mid = msgname2id(msgid)
            if mid is None:
                raise UNIMessageError(f"Unknown msgname {msgid}")
            msgid = mid
        self._msgid = msgid
        self.cpuidle = cpuidle
        self.timeref = timeref
        self.timestatus = timestatus
        if wno is None or tow is None:  # default to now
            wno, tow, leapsecond = utc2wnotow()
        self.wno = wno
        self.tow = tow
        self.version = version
        self.leapsecond = leapsecond
        self.delay = delay
        self._mode = msgmode
        self._payload = kwargs.get("payload", b"")
        self._parsebf = parsebitfield  # parsing bitfields Y/N?
        self._offset = 0  # payload offset in bytes
        self._index = []  # array of (nested) group indices
        self._suffix = ""  # attribute index suffix ("_01", "_02", etc.)

        pdict = self._get_dict(**kwargs)  # get appropriate payload dict
        for anam in pdict:  # process each attribute in dict
            self._set_attribute(anam, pdict, **kwargs)
        self._do_len_checksum()

        self._immutable = True  # once initialised, object is immutable

    def _set_attribute(self, anam: str, pdict: dict, **kwargs):  #  -> tuple:
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
                    self._set_attribute_bitfield(adef, **kwargs)
                else:  # treat bitfield as a single byte array
                    self._set_attribute_single(anam, numr, **kwargs)
            else:  # repeating group of attributes
                self._set_attribute_group(adef, **kwargs)
        else:  # single attribute
            self._set_attribute_single(anam, adef, **kwargs)

    def _set_attribute_group(self, adef: tuple, **kwargs):
        """
        Process (nested) group of attributes.

        :param tuple adef: attribute definition - tuple of (num repeats, attribute dict)
        :param int offset: payload offset in bytes
        :param list index: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (offset, index[])
        :rtype: tuple

        """

        self._index.append(0)  # add a (nested) group index
        anam, gdict = adef  # attribute signifying group size, group dictionary
        # derive or retrieve number of items in group
        if isinstance(anam, int):  # fixed number of repeats
            gsiz = anam
        elif anam == FREQNO:  # SATSINFO frequency group (assumes always at least 1)
            if "payload" in kwargs:
                gsiz = bytes2val(self._payload[self._offset + 3 : self._offset + 4], U1)
            else:
                gsiz = kwargs.get(f"{FREQNO}_{self._index[0]:02d}_01", 1)
        elif anam == "None":  # number of repeats 'variable by size'
            gsiz = self._calc_num_repeats(gdict, self._payload, self._offset, 0)
        else:  # number of repeats is defined in named attribute
            gsiz = getattr(self, anam)
        # recursively process each group attribute,
        # incrementing the payload offset and index as we go
        for i in range(gsiz):
            self._index[-1] = i + 1
            for key1 in gdict:
                self._set_attribute(key1, gdict, **kwargs)

        self._index.pop()  # remove this (nested) group index

    def _set_attribute_single(self, anam: str, adef: str | list, **kwargs):
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

        # if attribute is part of a (nested) repeating group, suffix name with index
        anami = anam
        for i in self._index:  # one index for each nested level
            if i > 0:
                anami += f"_{i:02d}"

        # determine attribute size (bytes) - some attributes have
        # variable length, depending on
        # - multiple of value of preceding attribute
        # - payload length - offset
        asiz = attsiz(adef)

        # if attribute is scaled
        if "*" in adef:
            adef, scaling = adef.split("*", 1)
            scaling = float(scaling)
        else:
            scaling = 1

        # if payload keyword has been provided,
        # use the appropriate offset of the payload
        if "payload" in kwargs:
            valb = self._payload[self._offset : self._offset + asiz]
            if scaling == 1:
                val = bytes2val(valb, adef)
            else:
                val = round(bytes2val(valb, adef) / scaling, SCALROUND)
        else:
            # if individual keyword has been provided,
            # set to provided value, else set to
            # nominal value
            val = kwargs.get(anami, nomval(adef))
            if scaling == 1:
                valb = val2bytes(val, adef)
            else:
                valb = val2bytes(int(val * scaling), adef)
            self._payload += valb

        setattr(self, anami, val)
        self._offset += asiz

    def _set_attribute_bitfield(self, atyp: str, **kwargs):
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
            bitfield = int.from_bytes(
                self._payload[self._offset : self._offset + bsiz], "little"
            )
        else:
            bitfield = 0

        # process each flag in bitfield
        for key, keyt in bdict.items():
            bitfield, bfoffset = self._set_attribute_bits(
                bitfield, bfoffset, key, keyt, self._index, **kwargs
            )

        # update payload
        if "payload" not in kwargs:
            self._payload += bitfield.to_bytes(bsiz, "little")

        self._offset += bsiz

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

        # if attribute is scaled
        if "*" in keyt:
            keyt, scaling = keyt.split("*", 1)
            scaling = float(scaling)
        else:
            scaling = 1

        atts = attsiz(keyt)  # determine flag size in bits

        if "payload" in kwargs:
            val = (bitfield >> bfoffset) & ((1 << atts) - 1)
            if self.identity in ("OBSVMCMP", "OBSVHCMP") and key == "psrstd":
                val = PSRSTD[val]
            elif self.identity in ("OBSVMCMP", "OBSVHCMP") and key == "adrstd":
                val = round((val + 1) / 512, SCALROUND)
            elif self.identity in ("OBSVMCMP", "OBSVHCMP") and key == "cno":
                val += 20
            elif scaling != 1:
                val = round(val / scaling, SCALROUND)
        else:
            if scaling == 1:
                val = kwargs.get(keyr, 0)
            else:
                val = int(kwargs.get(keyr, 0) * scaling)
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
            if self._mode == POLL:  # pragma: no cover
                pdict = UNI_PAYLOADS_POLL[self.identity]
            elif self._mode == SET:  # pragma: no cover
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
                stg += att + "=" + str(val).rstrip()
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
            umsg_name = f"{self._msgid}-NOMINAL"
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
