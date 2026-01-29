pyunigps
=======

[Current Status](#currentstatus) |
[Installation](#installation) |
[Message Categories](#msgcat) |
[Reading](#reading) |
[Parsing](#parsing) |
[Generating](#generating) |
[Serializing](#serializing) |
[Examples](#examples) |
[Extensibility](#extensibility) |
[Troubleshooting](#troubleshoot) |
[Author & License](#author)

# WORK IN PROGRESS - NOT YET FOR PRODUCTION USE

`pyunigps` is an original Python 3 parser for the UNI &copy; protocol. UNI is our term for the proprietary binary protocol implemented on Unicore &trade; GNSS receiver modules. `pyunigps` can also parse NMEA 0183 &copy; and RTCM3 &copy; protocols via the underlying [`pynmeagps`](https://github.com/semuconsulting/pynmeagps) and [`pyrtcm`](https://github.com/semuconsulting/pyrtcm) packages from the same author - hence it covers all the protocols that Unicore UNI GNSS receivers are capable of outputting.

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

This pre-alpha release implements functional UNI parse and construct methods via UNIReader and UNIMessage classes, but
does not yet include all 79 documented UNI payload definitions. These are on the backlog and will be completed and tested as and when time permits. Refer to [UNI_MSGIDS in unitypes_core.py](https://github.com/semuconsulting/pyunigps/blob/main/src/pyunigps/unitypes_core.py#L86) for the complete list of message definitions currently on the backlog. UNI protocol information sourced from public domain Unicore GNSS Protocol Specification © 2023, Unicore.

Sphinx API Documentation in HTML format is available at [https://www.semuconsulting.com/pyunigps/](https://www.semuconsulting.com/pyunigps/).

Contributions welcome - please refer to [CONTRIBUTING.MD](https://github.com/semuconsulting/pyunigps/blob/master/CONTRIBUTING.md).

[Bug reports](https://github.com/semuconsulting/pyunigps/blob/master/.github/ISSUE_TEMPLATE/bug_report.md) and [Feature requests](https://github.com/semuconsulting/pyunigps/blob/master/.github/ISSUE_TEMPLATE/feature_request.md) - please use the templates provided. For general queries and advice, post a message to one of the [pynmeagps Discussions](https://github.com/semuconsulting/pyunigps/discussions) channels.

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

For [Conda](https://docs.conda.io/en/latest/) users, `pyunigps` will in due course be made available from [conda forge](https://github.com/conda-forge/pyunigps-feedstock):

[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pyunigps/badges/version.svg)](https://anaconda.org/conda-forge/pyunigps)
[![Anaconda-Server Badge](https://img.shields.io/conda/dn/conda-forge/pyunigps)](https://anaconda.org/conda-forge/pyunigps)

```shell
conda install -c conda-forge pyunigps
```
---
## <a name="msgcat">UNI Message Categories - GET, SET, POLL</a>

**NB: following may change in final version:**

`pyunigps` divides UNI messages into three categories, signified by the `mode` or `msgmode` parameter.

| mode        | description                              | defined in         |
|-------------|------------------------------------------|--------------------|
| GET (0x00)  | output *from* the receiver (the default) | `unitypes_get.py`  |
| SET (0x01)  | command input *to* the receiver          | `unitypes_set.py`  |
| POLL (0x02) | query input *to* the receiver            | `unitypes_poll.py` |

If you're simply streaming and/or parsing the *output* of a UNI receiver, the mode is implicitly GET. If you want to create
or parse an *input* (command or query) message, you must set the mode parameter to SET or POLL. If the parser mode is set to
0x03 (SETPOLL), `pyunigps` will automatically determine the applicable input mode (SET or POLL) based on the message payload. See examples below for usage.

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
* `msgmode`: `GET` (0) (default), `SET` (1), `POLL` (2), `SETPOLL` (3) = automatically determine SET or POLL input mode

Example A -  Serial input. This example will output both UNI and NMEA messages but not RTCM3, and log any errors:
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
    raw_data, parsed_data = unr.read()
    if parsed_data is not None:
        print(parsed_data)
```
```
<UNI(VERSION, cpuidle=0, timeref=0, timestatus=0, wno=2406, tow=34534543, version=0, leapsecond=0, delay=0, device=M982, swversion=R4.10Build5251, authtype=HRPT00-S10C-P, psn=-, efuseid=ffff48ffff0fffff, comptime=2021/11/26)>
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
```
<UNI(VERSION, cpuidle=0, timeref=0, timestatus=0, wno=2406, tow=34534543, version=0, leapsecond=0, delay=0, device=M982, swversion=R4.10Build5251, authtype=HRPT00-S10C-P, psn=-, efuseid=ffff48ffff0fffff, comptime=2021/11/26)> 
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
```
<UNI(VERSION, cpuidle=0, timeref=0, timestatus=0, wno=2406, tow=34534543, version=0, leapsecond=0, delay=0, device=M982, swversion=R4.10Build5251, authtype=HRPT00-S10C-P, psn=-, efuseid=ffff48ffff0fffff, comptime=2021/11/26)>
```

---
## <a name="parsing">Parsing</a>

```
pyunigps.UNIreader.UNIReader.parse(message: bytes, **kwargs)
```

You can parse individual UNI messages using the static `UNIReader.parse(data)` function, which takes a bytes array containing a binary UNI message and returns a `UNIMessage` object.

**NB:** Once instantiated, a `UNIMessage` object is immutable.

The `parse()` method accepts the following optional keyword arguments:

* `msgmode`: `GET` (0) (default), `SET` (1), `POLL` (2), `SETPOLL` (3) = automatically determine SET or POLL input mode
* `validate`: VALCKSUM (0x01) = validate checksum (default), VALNONE (0x00) = ignore invalid checksum or length
* `parsebitfield`: 1 = parse bitfields ('X' type properties) as individual bit flags, where defined (default), 0 = leave bitfields as byte sequences

Example A - parsing VERSION output message:
```python
from pyunigps import GET, VALCKSUM, UNIReader

msg = UNIReader.parse(
    b'\xaaD\xb5\x00\x11\x004\x01\x00\x00f\t\x8f\xf4\x0e\x02\x00\x00\x00\x00\x00\x00\x00\x00M982R4.10Build5251                   HRPT00-S10C-P                                                                                                                    -                                                                 ffff48ffff0fffff                 2021/11/26                                 #\x87\x83\xb9'
        ,
    msgmode=GET,  # this is the default so could be omitted here
    validate=VALCKSUM,
    parsebitfield=1,
)
print(msg)
```
```
<UNI(VERSION, cpuidle=0, timeref=0, timestatus=0, wno=2406, tow=34534543, version=0, leapsecond=0, delay=0, device=M982, swversion=R4.10Build5251, authtype=HRPT00-S10C-P, psn=-, efuseid=ffff48ffff0fffff, comptime=2021/11/26)>
```

The `UNIMessage` object exposes different public attributes depending on its message type or 'identity',
e.g. the `VERSION` message has the following attributes:

```python
print(msg)
print(msg.identity)
print(swversion)
print(comptime)
```
```
<UNI(VERSION, cpuidle=0, timeref=0, timestatus=0, wno=2406, tow=34534543, version=0, leapsecond=0, delay=0, device=M982, swversion=R4.10Build5251, authtype=HRPT00-S10C-P, psn=-, efuseid=ffff48ffff0fffff, comptime=2021/11/26)>
VERSION
R4.10Build5251
2021/11/26
```

The `payload` attribute always contains the raw payload as bytes. Attributes within repeating groups are parsed with a two-digit suffix (svid_01, svid_02, etc.).

---
## <a name="generating">Generating</a>

```
class pyunigps.UNImessage.UNIMessage(msggrp, msgid, **kwargs)
```

You can create a `UNIMessage` object by calling the constructor with the following parameters:
1. message group (must be a valid group from `pyunigps.UNI_MSGIDS`)
2. message id (must be a valid id from `pyunigps.UNI_MSGIDS`)
3. (optional) a series of keyword parameters representing the message payload
4. (optional) `parsebitfield` keyword - 1 = define bitfields as individual bits (default), 0 = define bitfields as byte sequences

The 'message group' and 'message id' parameters must be passed as bytes.

The message payload can be defined via keyword arguments in one of three ways:
1. A single keyword argument of `payload` containing the full payload as a sequence of bytes (any other keyword arguments will be ignored). **NB** the `payload` keyword argument *must* be used for message types which have a 'variable by size' repeating group.
2. One or more keyword arguments corresponding to individual message attributes. Any attributes not explicitly provided as keyword arguments will be set to a nominal value according to their type.
3. If no keyword arguments are passed, the payload is assumed to be null.

Example A - generate a VERSION message from individual keyword arguments:

```python
from pyunigps import UNIMessage
msg = UNIMessage(
    msgid=17,
    wno=2406,
    tow=34534543,
    device="M982",
    swversion="R4.10Build5251",
    authtype="HRPT00-S10C-P",
    psn="-",
    efuseid="ffff48ffff0fffff",
    comptime="2021/11/26",
)
print(msg)
```
```
<UNI(VERSION, cpuidle=0, timeref=0, timestatus=0, wno=2406, tow=34534543, version=0, leapsecond=0, delay=0, device=M982, swversion=R4.10Build5251, authtype=HRPT00-S10C-P, psn=-, efuseid=ffff48ffff0fffff, comptime=2021/11/26)>
```

---
## <a name="serializing">Serializing</a>

The `UNIMessage` class implements a `serialize()` method to convert a `UNIMessage` object to a bytes array suitable for writing to an output stream.

e.g. to create and send a `RAW-PPPB2B` message:

```python
from serial import Serial
from pyunigps import UNIMessage
serialOut = Serial('COM7', 115200, timeout=5)
print(msg)
output = msg.serialize()
print(output)
serialOut.write(output)
```
```
<UNI(VERSION, cpuidle=0, timeref=0, timestatus=0, wno=2406, tow=34534543, version=0, leapsecond=0, delay=0, device=M982, swversion=R4.10Build5251, authtype=HRPT00-S10C-P, psn=-, efuseid=ffff48ffff0fffff, comptime=2021/11/26)>
b'\xaaD\xb5\x00\x11\x004\x01\x00\x00f\t\x8f\xf4\x0e\x02\x00\x00\x00\x00\x00\x00\x00\x00M982R4.10Build5251                   HRPT00-S10C-P                                                                                                                    -                                                                 ffff48ffff0fffff                 2021/11/26                                 #\x87\x83\xb9'  
```

---
## <a name="examples">Examples</a>

The following command line examples can be found in the `\examples` folder:

1. [`uniusage.py`](https://github.com/semuconsulting/pyunigps/blob/main/examples/uniusage.py) illustrates basic usage of the `UNIMessage` and `UNIReader` classes.

---
## <a name="extensibility">Extensibility</a>

The UNI protocol is principally defined in the modules `unitypes_*.py` as a series of dictionaries. Message payload definitions must conform to the following rules:

```
1. attribute names must be unique within each message class
2. attribute types must be one of the valid types (S1, U2, X4, etc.)
3. if the attribute is scaled, attribute type is list of [attribute type as string (S1, U2, etc.), scaling factor as float] e.g. {"lat": [I4, 1e-7]}
4. repeating or bitfield groups must be defined as a tuple ('numr', {dict}), where:
   'numr' is either:
     a. an integer representing a fixed number of repeats e.g. 32
     b. a string representing the name of a preceding attribute containing the number of repeats e.g. 'numCh'
     c. an 'X' attribute type ('X1', 'X2', 'X4', etc) representing a group of individual bit flags
     d. 'None' for a 'variable by size' repeating group. Only one such group is permitted per payload and it must be at the end.
   {dict} is the nested dictionary of repeating items or bitfield group
```

Repeating attribute names are parsed with a two-digit suffix (svid_01, svid_02, etc.). Nested repeating groups are supported.

---
## <a name="troubleshoot">Troubleshooting</a>

#### 1. `UnicodeDecode` errors.
- If reading UNI data from a log file, check that the file.open() procedure is using the `rb` (read binary) setting e.g.
`stream = open('unidata.log', 'rb')`.

---
## <a name="author">Author & License Information</a>

semuadmin@semuconsulting.com

![License](https://img.shields.io/github/license/semuconsulting/pyunigps.svg)

`pyunigps` is maintained entirely by unpaid volunteers. It receives no funding from advertising or corporate sponsorship. If you find the utility useful, please consider sponsoring the project with the price of a coffee...

[![Sponsor](https://github.com/semuconsulting/pyubx2/blob/master/images/sponsor.png?raw=true)](https://buymeacoffee.com/semuconsulting)
