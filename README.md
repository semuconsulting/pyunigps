pyunigps
=======

[Current Status](#currentstatus) |
[Installation](#installation) |
[Reading](#reading) |
[Parsing](#parsing) |
[Generating](#generating) |
[Serializing](#serializing) |
[Examples](#examples) |
[Extensibility](#extensibility) |
[Author & License](#author)

`pyunigps` is an original Python 3 parser for the UNI protocol. UNI is our term for the proprietary binary data output protocol implemented on Unicore &trade; GNSS receiver modules. `pyunigps` can also parse NMEA 0183 &copy; and RTCM3 &copy; protocols via the underlying [`pynmeagps`](https://github.com/semuconsulting/pynmeagps) and [`pyrtcm`](https://github.com/semuconsulting/pyrtcm) packages from the same author, covering all the protocols that Unicore UNI GNSS receivers are capable of outputting.

The `pyunigps` homepage is located at [https://github.com/semuconsulting/pyunigps](https://github.com/semuconsulting/pyunigps).

This is an independent project and we have no affiliation whatsoever with Unicore.

## <a name="currentstatus">Current Status</a>

![Status](https://img.shields.io/pypi/status/pyunigps)
![Release](https://img.shields.io/github/v/release/semuconsulting/pyunigps?include_prereleases)
![Build](https://img.shields.io/github/actions/workflow/status/semuconsulting/pyunigps/main.yml?branch=main)
![Codecov](https://img.shields.io/codecov/c/github/semuconsulting/pyunigps)
![Release Date](https://img.shields.io/github/release-date-pre/semuconsulting/pyunigps)
![Last Commit](https://img.shields.io/github/last-commit/semuconsulting/pyunigps)
![Contributors](https://img.shields.io/github/contributors/semuconsulting/pyunigps.svg)
![Open Issues](https://img.shields.io/github/issues-raw/semuconsulting/pyunigps)

`pyunigps` implements a comprehensive set of messages for Unicore "NebulasIV" High Precision GPS/GNSS devices, including the UM96n and UM98n series, but is readily [extensible](#extensibility). Refer to [UNI_MSGIDS in unitypes_core.py](https://github.com/semuconsulting/pyunigps/blob/main/src/pyunigps/unitypes_core.py#L86) for the complete list of message definitions currently defined. UNI protocol information sourced from public domain Unicore Reference Commands R1.13 © Dec 2025 Unicore
https://en.unicore.com/uploads/file/Unicore%20Reference%20Commands%20Manual%20For%20N4%20High%20Precision%20Products_V2_EN_R1.13.pdf

**FYI:**

Unicore "NebulasIV" GNSS receivers are configured using TTY commands (ASCII text over serial port) e.g. `"SATSINFOB COM1 1"`. The command response will be an ASCII text message resembling an NMEA sentence e.g. `"$command,SATSINFOB COM1 1,response: OK*46"` or 
`"$command,SATSXXXXB COM1 1,response: PARSING FAILD NO MATCHING FUNC  SATSXXXXB*01"`.

Sphinx API Documentation in HTML format is available at [https://www.semuconsulting.com/pyunigps/](https://www.semuconsulting.com/pyunigps/).

Contributions welcome - please refer to [CONTRIBUTING.MD](https://github.com/semuconsulting/pyunigps/blob/master/CONTRIBUTING.md).

[Bug reports](https://github.com/semuconsulting/pyunigps/blob/master/.github/ISSUE_TEMPLATE/bug_report.md) and [Feature requests](https://github.com/semuconsulting/pyunigps/blob/master/.github/ISSUE_TEMPLATE/feature_request.md) - please use the templates provided. For general queries and advice, post a message to one of the [pyunigps Discussions](https://github.com/semuconsulting/pyunigps/discussions) channels.

![No Copilot](https://github.com/semuconsulting/PyGPSClient/blob/master/images/nocopilot100.png?raw=true)

---
## <a name="installation">Installation</a>

![Python version](https://img.shields.io/pypi/pyversions/pyunigps.svg?style=flat)
[![PyPI version](https://img.shields.io/pypi/v/pyunigps.svg?style=flat)](https://pypi.org/project/pyunigps/)
[![PyPI downloads](https://github.com/semuconsulting/pygpsclient/blob/master/images/clickpy_icon.svg?raw=true)](https://clickpy.clickhouse.com/dashboard/pyunigps)

`pyunigps` is compatible with Python>=3.10. In the following, `python3` & `pip` refer to the Python 3 executables. You may need to substitute `python` for `python3`, depending on your particular environment (*on Windows it's generally `python`*).

The recommended way to install the latest version of `pyunigps` is with [pip](http://pypi.python.org/pypi/pip/):

```shell
python3 -m pip install --upgrade pyunigps
```

If required, `pyunigps` can also be installed into a virtual environment, e.g.:

```shell
python3 -m venv env
source env/bin/activate # (or env\Scripts\activate on Windows)
python3 -m pip install --upgrade pyunigps
```

For [Conda](https://docs.conda.io/en/latest/) users, `pyunigps` is available from [conda forge](https://github.com/conda-forge/pyunigps-feedstock):

[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pyunigps/badges/version.svg)](https://anaconda.org/conda-forge/pyunigps)
[![Anaconda-Server Badge](https://img.shields.io/conda/dn/conda-forge/pyunigps)](https://anaconda.org/conda-forge/pyunigps)

```shell
conda install -c conda-forge pyunigps
```
---

## <a name="reading">Reading (Streaming)</a>

```
class pyunigps.UNIreader.UNIReader(stream, *args, **kwargs)
```

You can create a `UNIReader` object by calling the constructor with an active stream object. 
The stream object can be any viable data stream which supports a `read(n) -> bytes` method (e.g. File or Serial, with 
or without a buffer wrapper). `pyunigps` implements an internal `SocketWrapper` class to allow sockets to be read in the same way as other streams (see example below).

Individual UNI messages can then be read using the `UNIReader.read()` function, which returns both the raw binary data (as bytes) and the parsed data (as a `UNIMessage` object, via the `parse()` method). The function is thread-safe in so far as the incoming data stream object is thread-safe. `UNIReader` also implements an iterator.

The constructor accepts the following optional keyword arguments:

* `protfilter`: `NMEA_PROTOCOL` (1), `UNI_PROTOCOL` (2), `RTCM3_PROTOCOL` (4). Can be OR'd; default is `NMEA_PROTOCOL | UNI_PROTOCOL | RTCM3_PROTOCOL` (7)
* `quitonerror`: `ERR_IGNORE` (0) = ignore errors, `ERR_LOG` (1) = log errors and continue (default), `ERR_RAISE` (2) = (re)raise errors and terminate
* `validate`: `VALCKSUM` (0x01) = validate checksum (default), `VALNONE` (0x00) = ignore invalid checksum or length
* `parsebitfield`: 1 = parse bitfields ('X' type properties) as individual bit flags, where defined (default), 0 = leave bitfields as byte sequences
* `msgmode`: `GET` (0) (default), `SET` (1), `POLL` (2)

Example A -  Serial input (using iterator). This example will output both UNI and NMEA messages but not RTCM3, and log any errors:
```python
from serial import Serial

from pyunigps import ERR_LOG, NMEA_PROTOCOL, UNI_PROTOCOL, VALCKSUM, UNIReader

with Serial("/dev/ttyACM0", 115200, timeout=3) as stream:
    unr = UNIReader(
        stream,
        protfilter=UNI_PROTOCOL | NMEA_PROTOCOL,
        quitonerror=ERR_LOG,
        validate=VALCKSUM,
        parsebitfield=1,
    )
    for raw_data, parsed_data in unr:
        print(parsed_data)
```
```
<UNI(SATSINFO, cpuidle=96, timeref=1, timestatus=1, wno=2215, tow=367199000, version=0, leapsecond=18, delay=16, numsat=50, reserved1=0, reserved2=0, reserved3=0, L1B1IE1=1, L2CL2B2IE5b=1, L5B3IE5aL5=0, B1CL1C=1, B2aG3E6=0, B2bL2P=1, prn_01=2, azi_01=302, elev_01=51, sysstatus_01_01=0, cno_01_01=45, freqstatus_01_01=0, freqno_01_01=2, sysstatus_01_02=0, cno_01_02=42, freqstatus_01_02=9, freqno_01_02=2, ... prn_50=36, azi_50=286, elev_50=19, sysstatus_50_01=3, cno_50_01=34, freqstatus_50_01=2, freqno_50_01=3, sysstatus_50_02=3, cno_50_02=42, freqstatus_50_02=17, freqno_50_02=3, sysstatus_50_03=3, cno_50_03=38, freqstatus_50_03=12, freqno_50_03=3)>
```

Example B - File input (using iterator). This will only output UNI data, and fail on any error:
```python
from pyunigps import ERR_RAISE, UNI_PROTOCOL, VALCKSUM, UNIReader

with open("pygpsdata_u980.log", "rb") as stream:
    unr = UNIReader(
        stream, protfilter=UNI_PROTOCOL, validate=VALCKSUM, quitonerror=ERR_RAISE
    )
    for raw_data, parsed_data in unr:
        print(parsed_data)
```

Example C - Socket input (using iterator). This will output UNI, NMEA and RTCM3 data, and ignore any errors:
```python
import socket

from pyunigps import (
    ERR_IGNORE,
    NMEA_PROTOCOL,
    UNI_PROTOCOL,
    RTCM3_PROTOCOL,
    VALCKSUM,
    UNIReader,
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
    stream.connect(("localhost", 50007))
    unr = UNIReader(
        stream,
        protfilter=NMEA_PROTOCOL | UNI_PROTOCOL | RTCM3_PROTOCOL,
        validate=VALCKSUM,
        quitonerror=ERR_IGNORE,
    )
    for raw_data, parsed_data in unr:
        print(parsed_data)

```

---
## <a name="parsing">Parsing</a>

```
pyunigps.UNIreader.UNIReader.parse(message: bytes, **kwargs)
```

You can parse individual UNI messages using the static `UNIReader.parse(data)` function, which takes a bytes array containing a binary UNI message and returns a `UNIMessage` object.

**NB:** Once instantiated, a `UNIMessage` object is immutable.

The `parse()` method accepts the following optional keyword arguments:

* `validate`: VALCKSUM (0x01) = validate checksum (default), VALNONE (0x00) = ignore invalid checksum or length
* `parsebitfield`: 1 = parse bitfields ('X' type properties) as individual bit flags, where defined (default), 0 = leave bitfields as byte sequences
* `msgmode`: `GET` (0) (default), `SET` (1), `POLL` (2)

Example A - parsing BESTNAV output message:
```python
from pyunigps import GET, VALCKSUM, UNIReader

msg = UNIReader.parse(
    b"\xaaD\xb5YF\x08x\x00\x00\xa0e\t\xe8\...\x98\x15\xa5\xf1",
    validate=VALCKSUM,
    parsebitfield=1,
)
print(msg)
```
```
"<UNI(BESTNAV, cpuidle=89, timeref=0, timestatus=160, wno=2405, tow=75521000, version=0, leapsecond=18, delay=13, solstatus=0, postype=16, lat=43.450634678833644, lon=-1.1303087675041795, hmsl=36.32093767914921, undulation=51.67765808105469, datumid=61, latstd=2.6222991943359375, lonstd=1.9253981113433838, hmslstd=2.7721946239471436, stationid=0, diffage=0.0, solage=0.0, numsvs=25, numsolnsvs=21, reserved1=21, reserved2=0, reserved3=1, rtkverify=0, psrionocorr=1, gale1=1, gale5b=0, gale5a=0, bdsb1l=1, bdsb3l=0, bdsb2a=0, bdsb1c=0, gpsl1=1, gpsl2=0, gpsl5=0, glol1=1, glol2=0, bdsb2l=0, vsolstatus=0, veltype=8, latency=0.0, age=0.0, horspd=0.06034742542911377, trkgnd=192.53216796929004, vertspd=-0.001533079795667136, verspdstd=0.14649531245231628, horspdstd=0.11643162369728088)>"      
```

The `UNIMessage` object exposes different public attributes depending on its message type or 'identity'. Helper methods are available to convert position coordinates into different formats. Attributes which are enumerations may have corresponding decodes in `pyunigps.unitypes_decodes` e.g. the `BESTNAV` message has the following attributes:

```python
from pyunigps import POSTYPE, PSRIONOCORR, SOLSTATUS, latlon2dms, llh2iso6709, wnotow2utc
print(msg.identity)
print(wnotow2utc(msg.wno, msg.tow, msg.leapsecond))
print(msg.lat, msg.lon, msg.hmsl)
print(latlon2dms(msg.lat, msg.lon))
print(llh2iso6709(msg.lat, msg.lon, msg.hmsl))
print(msg.solstatus, SOLSTATUS[msg.solstatus])
print(msg.postype, POSTYPE[msg.postype])
print(msg.psrionocorr, PSRIONOCORR[msg.psrionocorr])
```
```
BESTNAV
2026-02-08 20:58:23+00:00
43.450634678833644, -1.1303087675041795, 36.32093767914921
('43°27′2.28484″N', '1°7′49.11156″W')
+43.450634678833644-1.1303087675041794+36.32093767914921CRSWGS_84/
0 SOL_COMPUTED
16 SINGLE
1 Klobuchareph
```

The `payload` attribute always contains the raw payload as bytes. Attributes within repeating groups are parsed with a two-digit suffix (prn_01, prn_02, etc.).

---
## <a name="generating">Generating</a>

```
class pyunigps.UNImessage.UNIMessage(msggrp, msgid, **kwargs)
```

You can create a `UNIMessage` object by calling the constructor with the following parameters:
1. message id in each integer or string format (must be a valid id or name from `pyunigps.UNI_MSGIDS`)
2. (optional) a series of keyword parameters representing the message header and payload.
3. (optional) `parsebitfield` keyword - 1 = define bitfields as individual bits (default), 0 = define bitfields as byte sequences.

The message payload can be defined via keyword arguments in one of three ways:
1. A single keyword argument of `payload` containing the full payload as a sequence of bytes (any other keyword arguments will be ignored). **NB** the `payload` keyword argument *must* be used for message types which have a 'variable by size' repeating group.
2. One or more keyword arguments corresponding to individual message attributes. Any attributes not explicitly provided as keyword arguments will be set to a nominal value according to their type.
3. If no keyword arguments are passed, the payload is assumed to be null.
4. If the `wno` or `tow` arguments are omitted, they will default to the current datetime and leapsecond offset.

Example A - generate a VERSION message from individual keyword arguments:

```python
from pyunigps import UNIMessage
msg = UNIMessage(
    msgid=17,
    wno=2406,
    tow=34534543,
    device=18,
    swversion="R4.10Build5251",
    authtype="HRPT00-S10C-P",
    psn="-",
    efuseid="ffff48ffff0fffff",
    comptime="2021/11/26",
)
print(msg)
```
```
<UNI(VERSION, cpuidle=0, timeref=0, timestatus=0, wno=2406, tow=34534543, version=0, leapsecond=18, delay=0, device=18, swversion=R4.10Build5251, authtype=HRPT00-S10C-P, psn=-, efuseid=ffff48ffff0fffff, comptime=2021/11/26)>
```

---
## <a name="serializing">Serializing</a>

The `UNIMessage` class implements a `serialize()` method to convert a `UNIMessage` object to a bytes array suitable for writing to an output stream.

e.g. to serialize and send a `VERSION` message:

```python
from serial import Serial
from pyunigps import UNIMessage
serialOut = Serial('COM1', 115200, timeout=5)
print(msg)
output = msg.serialize()
print(output)
serialOut.write(output)
```
```
<UNI(VERSION, cpuidle=0, timeref=0, timestatus=0, wno=2406, tow=34534543, version=0, leapsecond=18, delay=0, device=18, swversion=R4.10Build5251, authtype=HRPT00-S10C-P, psn=-, efuseid=ffff48ffff0fffff, comptime=2021/11/26)>
b'\xaaD\xb5\x00\x11\x004\x01\x00\x00f\t\x8f\xf4\x0e\x02\x00\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x00R4.10Build5251                   HRPT00-S10C-P                                                                                                                    -                                                                 ffff48ffff0fffff                 2021/11/26                                 \x11t\x19\x1f'
```

---
## <a name="examples">Examples</a>

The following command line examples can be found in the `\examples` folder:

1. [`uniusage.py`](https://github.com/semuconsulting/pyunigps/blob/main/examples/uniusage.py) illustrates basic usage of the `UNIMessage` and `UNIReader` classes.
1. [`unipoller.py`](https://github.com/semuconsulting/pyunigps/blob/main/examples/unipoller.py) illustrates how to stream UNI messages while simultaneously applying ASCII text configuration commands.

---
## <a name="extensibility">Extensibility</a>

The UNI protocol is principally defined in the modules `unitypes_*.py` as a series of dictionaries. Message payload definitions must conform to the following rules:

```
1. attribute names must be unique within each message class
2. attribute types must be one of the valid types (S1, U2, X4, etc.). A suffix of "*f" signifies a scaling factor of f is to be applied to the raw value.
3. repeating or bitfield groups must be defined as a tuple ('numr', {dict}), where:
   'numr' is either:
     a. an integer representing a fixed number of repeats e.g. 32
     b. a string representing the name of a preceding attribute containing the number of repeats e.g. 'numsat'
     c. an 'X' attribute type ('X1', 'X2', 'X4', etc) representing a group of individual bit flags
     d. 'None' for a 'variable by size' repeating group. Only one such group is permitted per payload and it must be at the end.
   {dict} is the nested dictionary of repeating items or bitfield group
```

Repeating attribute names are parsed with a two-digit suffix (prn_01, prn_02, etc.). Nested repeating groups are supported.

---
## <a name="author">Author & License Information</a>

semuadmin@semuconsulting.com

![License](https://img.shields.io/github/license/semuconsulting/pyunigps.svg)

`pyunigps` is maintained entirely by unpaid volunteers. It receives no funding from advertising or corporate sponsorship. If you find the utility useful, please consider sponsoring the project with the price of a coffee...

[![Sponsor](https://github.com/semuconsulting/pyubx2/blob/master/images/sponsor.png?raw=true)](https://buymeacoffee.com/semuconsulting)
