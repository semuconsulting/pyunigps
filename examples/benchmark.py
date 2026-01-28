"""
pyunigps Performance benchmarking utility

Usage (kwargs optional): python3 benchmark.py cycles=10000

Created on 19 May 2025

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2021
:license: BSD 3-Clause
"""

# pylint: disable=line-too-long

from io import BytesIO
from sys import argv
from time import process_time_ns
from platform import version as osver, python_version
from pyunigps.UNIreader import UNIReader
from pyunigps._version import __version__ as UNIver

UNIMESSAGES = [
    b"QG\x10\x01%\x00\x03\x82<\x00\x00\x00\x00\x00\x00ff\xdcA3c\xb2\xbd\x00\xdc&\xbe\xff\xff\xb79\xc7\xcf\xe3;\xa4\xe0\x90:\x7f\xda~\xbf+\xf2",
    b"QG\x01\x01\x04\x00\x03\x02\x00\x00\x0b9",
    b"QG\x01\x01\x04\x00\x02\x01\x00\x00\t2",
    b"QG\x01\x01\x04\x00\x02\x01\x00\x00\t2",
    b"QG\x10\x01%\x00\x03\x82<\x00\x00\x00\x00\x00\x00ff\xdcA3c\xb2\xbd\x00\xdc&\xbe\xff\xff\xb79\xc7\xcf\xe3;\xa4\xe0\x90:\x7f\xda~\xbf+\xf2",
    b"QG\x02\x01\x0c\x00\x01\x01\x00\x00\x00\x08\x07\x00\x08\x00\x01\x00)r",
    b"QG\x01\x01\x04\x00\x02\x01\x00\x00\t2",
    b"QG\x01\x01\x04\x00\x02\x04\x00\x00\x0c;",
    b"QG\x01\x01\x04\x00\x02\x04\x00\x00\x0c;",
    b"QG\x02\x04\x0c\x00\x00\x01\x00\x00@B\x0f\x00\x80\x84\x1e\x00\xc6\xff",
    b"QG\x01\x01\x04\x00\x02\x04\x00\x00\x0c;",
    b"QG\x01\x01\x04\x00\x02\x10\x00\x00\x18_",
    b"QG\x01\x01\x04\x00\x02\x10\x00\x00\x18_",
    b"QG\x01\x01\x04\x00\x02\x10\x00\x00\x18_",
    b"QG\x10\x01%\x00\x03\x82<\x00\x00\x00\x00\x00\x00ff\xdcA3c\xb2\xbd\x00\xdc&\xbe\xff\xff\xb79\xc7\xcf\xe3;\xa4\xe0\x90:\x7f\xda~\xbf+\xf2",
    b"QG\x02\x10\x05\x00\xf1\n\x00\x00\x03\x15\x95",
    b"QG\x01\x01\x04\x00\x02\x10\x00\x00\x18_",
    b"QG\x02\x10\x05\x00\xca\x01d\x00\x03I\xda",
    b"QG\x01\x01\x04\x00\x02\x10\x00\x00\x18_",
    b"QG\x01\x01\x04\x00\x02\x10\x00\x00\x18_",
    b"QG\x01\x01\x04\x00\x02\x10\x00\x00\x18_",
    b"QG\x10\x01%\x00\x03\x82<\x00\x00\x00\x00\x00\x00ff\xdcA3c\xb2\xbd\x00\xdc&\xbe\xff\xff\xb79\xc7\xcf\xe3;\xa4\xe0\x90:\x7f\xda~\xbf+\xf2",
    b"QG\x02\x10\x07\x00\x04\x00\xca\x02\x90\x01\x03}\xc0",
    b"QG\x01\x01\x04\x00\x02\x10\x00\x00\x18_",
    b"QG\x01\x01\x04\x00\x02 \x00\x00(\x8f",
    b"QG\x02 \x04\x00.\x00.\x00\x82\x1c",
    b"QG\x01\x01\x04\x00\x02 \x00\x00(\x8f",
    b"QG\x01\x01\x04\x00\x03\x01\x00\x00\n6",
    b"QG\x10\x01%\x00\x03\x82<\x00\x00\x00\x00\x00\x00ff\xdcA3c\xb2\xbd\x00\xdc&\xbe\xff\xff\xb79\xc7\xcf\xe3;\xa4\xe0\x90:\x7f\xda~\xbf+\xf2",
    b"QG\x01\x01\x04\x00\x03\x02\x00\x00\x0b9",
    b"QG\x01\x01\x04\x00\x03\x02\x00\x00\x0b9",
    b"QG\x06\x01$\x00LUA600A00AANR01A022023/04/1716:28:06\x06%",
    b"QG\x01\x01\x04\x00\x06\x01\x00\x00\rB",
    b"QG\x06\x02\x10\x00\x01Q29G0F222200666\\\x1e",
    b"QG\x01\x01\x04\x00\x06\x02\x00\x00\x0eE",
    b"QG\x10\x01%\x00\x03\x82<\x00\x00\x00\x00\x00\x00ff\xdcA3c\xb2\xbd\x00\xdc&\xbe\xff\xff\xb79\xc7\xcf\xe3;\xa4\xe0\x90:\x7f\xda~\xbf+\xf2",
]
msgb = b""
for msg in UNIMESSAGES:
    msgb += msg
UNIBYTES = msgb


def progbar(i: int, lim: int, inc: int = 20):
    """
    Display progress bar on console.

    :param int i: iteration
    :param int lim: max iterations
    :param int inc: bar increments (20)
    """

    i = min(i, lim)
    pct = int(i * inc / lim)
    if not i % int(lim / inc):
        print(
            f"{int(pct*100/inc):02}% " + "\u2593" * pct + "\u2591" * (inc - pct),
            end="\r",
        )


def benchmark(**kwargs) -> float:
    """
    pyrtcm Performance benchmark test.

    :param int cycles: (kwarg) number of test cycles (10,000)
    :returns: benchmark as transactions/second
    :rtype: float
    :raises: SBFStreamError
    """

    cyc = int(kwargs.get("cycles", 5000))
    txnc = len(UNIMESSAGES)
    txnt = txnc * cyc

    print(
        f"\nOperating system: {osver()}",
        f"\nPython version: {python_version()}",
        f"\npysbf2 version: {UNIver}",
        f"\nTest cycles: {cyc:,}",
        f"\nTxn per cycle: {txnc:,}",
    )

    start = process_time_ns()
    print(f"\nBenchmark test started at {start}")
    for i in range(cyc):
        progbar(i, cyc)
        stream = BytesIO(UNIBYTES)
        sbr = UNIReader(stream, parsing=True)
        for _, _ in sbr:
            pass
    end = process_time_ns()
    print(f"Benchmark test ended at {end}.")
    duration = end - start
    msglen = len(UNIBYTES) * cyc
    txs = round(txnt * 1e9 / duration, 2)
    kbs = round(msglen * 1e9 / duration / 2**10, 2)

    print(
        f"\n{txnt:,} messages processed in {duration/1e9:,.3f} seconds = {txs:,.2f} txns/second, {kbs:,.2f} kB/second.\n"
    )

    return txs, kbs


def main():
    """
    CLI Entry point.

    args as benchmark() method
    """

    benchmark(**dict(arg.split("=") for arg in argv[1:]))


if __name__ == "__main__":
    main()
