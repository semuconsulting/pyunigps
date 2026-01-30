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
from pyunigps.unireader import UNIReader
from pyunigps._version import __version__ as univer

UNIMESSAGES = [
    b"\xaa\x44\xb5\x00\xe8\xff\x05\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x01\x02\x03\x04\x05\xc1\xff\xd2\xaa",
    b'\xaaD\xb5\x00\xea\xff\x14\x00\x01\x00f\t\xaa\xdd\x13\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x03\x00\x08\x00"\x00\x0f\x007\x00\x17\x000\x00\xa2_\x8a\xd4'
    b"\xaaD\xb5\x00\x11\x004\x01\x00\x00f\t\x8f\xf4\x0e\x02\x00\x00\x00\x00\x00\x00\x00\x00M982R4.10Build5251                   HRPT00-S10C-P                                                                                                                    -                                                                 ffff48ffff0fffff                 2021/11/26                                 #\x87\x83\xb9"
    b"\xaa\x44\xb5\x00\xe8\xff\x05\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x01\x02\x03\x04\x05\xc1\xff\xd2\xaa",
    b'\xaaD\xb5\x00\xea\xff\x14\x00\x01\x00f\t\xaa\xdd\x13\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x03\x00\x08\x00"\x00\x0f\x007\x00\x17\x000\x00\xa2_\x8a\xd4'
    b"\xaaD\xb5\x00\x11\x004\x01\x00\x00f\t\x8f\xf4\x0e\x02\x00\x00\x00\x00\x00\x00\x00\x00M982R4.10Build5251                   HRPT00-S10C-P                                                                                                                    -                                                                 ffff48ffff0fffff                 2021/11/26                                 #\x87\x83\xb9"
    b"\xaa\x44\xb5\x00\xe8\xff\x05\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x01\x02\x03\x04\x05\xc1\xff\xd2\xaa",
    b'\xaaD\xb5\x00\xea\xff\x14\x00\x01\x00f\t\xaa\xdd\x13\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x03\x00\x08\x00"\x00\x0f\x007\x00\x17\x000\x00\xa2_\x8a\xd4'
    b"\xaaD\xb5\x00\x11\x004\x01\x00\x00f\t\x8f\xf4\x0e\x02\x00\x00\x00\x00\x00\x00\x00\x00M982R4.10Build5251                   HRPT00-S10C-P                                                                                                                    -                                                                 ffff48ffff0fffff                 2021/11/26                                 #\x87\x83\xb9"
    b"\xaa\x44\xb5\x00\xe8\xff\x05\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x01\x02\x03\x04\x05\xc1\xff\xd2\xaa",
    b'\xaaD\xb5\x00\xea\xff\x14\x00\x01\x00f\t\xaa\xdd\x13\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x03\x00\x08\x00"\x00\x0f\x007\x00\x17\x000\x00\xa2_\x8a\xd4'
    b"\xaaD\xb5\x00\x11\x004\x01\x00\x00f\t\x8f\xf4\x0e\x02\x00\x00\x00\x00\x00\x00\x00\x00M982R4.10Build5251                   HRPT00-S10C-P                                                                                                                    -                                                                 ffff48ffff0fffff                 2021/11/26                                 #\x87\x83\xb9"
    b"\xaa\x44\xb5\x00\xe8\xff\x05\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x01\x02\x03\x04\x05\xc1\xff\xd2\xaa",
    b'\xaaD\xb5\x00\xea\xff\x14\x00\x01\x00f\t\xaa\xdd\x13\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x03\x00\x08\x00"\x00\x0f\x007\x00\x17\x000\x00\xa2_\x8a\xd4'
    b"\xaaD\xb5\x00\x11\x004\x01\x00\x00f\t\x8f\xf4\x0e\x02\x00\x00\x00\x00\x00\x00\x00\x00M982R4.10Build5251                   HRPT00-S10C-P                                                                                                                    -                                                                 ffff48ffff0fffff                 2021/11/26                                 #\x87\x83\xb9"
    b"\xaa\x44\xb5\x00\xe8\xff\x05\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x01\x02\x03\x04\x05\xc1\xff\xd2\xaa",
    b'\xaaD\xb5\x00\xea\xff\x14\x00\x01\x00f\t\xaa\xdd\x13\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x03\x00\x08\x00"\x00\x0f\x007\x00\x17\x000\x00\xa2_\x8a\xd4'
    b"\xaaD\xb5\x00\x11\x004\x01\x00\x00f\t\x8f\xf4\x0e\x02\x00\x00\x00\x00\x00\x00\x00\x00M982R4.10Build5251                   HRPT00-S10C-P                                                                                                                    -                                                                 ffff48ffff0fffff                 2021/11/26                                 #\x87\x83\xb9"
    b"\xaa\x44\xb5\x00\xe8\xff\x05\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x01\x02\x03\x04\x05\xc1\xff\xd2\xaa",
    b'\xaaD\xb5\x00\xea\xff\x14\x00\x01\x00f\t\xaa\xdd\x13\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x03\x00\x08\x00"\x00\x0f\x007\x00\x17\x000\x00\xa2_\x8a\xd4'
    b"\xaaD\xb5\x00\x11\x004\x01\x00\x00f\t\x8f\xf4\x0e\x02\x00\x00\x00\x00\x00\x00\x00\x00M982R4.10Build5251                   HRPT00-S10C-P                                                                                                                    -                                                                 ffff48ffff0fffff                 2021/11/26                                 #\x87\x83\xb9"
    b"\xaa\x44\xb5\x00\xe8\xff\x05\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\x00\x11\x22\x33\x44\x55\x66\x01\x02\x03\x04\x05\xc1\xff\xd2\xaa",
    b'\xaaD\xb5\x00\xea\xff\x14\x00\x01\x00f\t\xaa\xdd\x13\x02\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x03\x00\x08\x00"\x00\x0f\x007\x00\x17\x000\x00\xa2_\x8a\xd4'
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
        f"\npyunigps version: {univer}",
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
