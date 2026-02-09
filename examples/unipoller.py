"""
unipoller.py

This example illustrates how to read and display UNI messages
while simultaneously sending ASCII configuration commands. This
represents a useful generic pattern for many end user applications.

Usage:

python3 unipoller.py port="/dev/ttyACM0" baudrate=115200 timeout=3
   protfilter=2 enable=1 sysport=COM1

Press CTRL-C to terminate.

FYI Unicore "NebulasIV" GNSS receivers like the UM980 are configured using
ASCII text commands e.g.

`SATSINFOB COM1 1`.

The command response will be an ASCII text message resembling an NMEA sentence e.g.

`$command,SATSINFOB COM1 1,response: OK*46`

or

`$command,SATSXXXXB COM1 1,response: PARSING FAILD NO MATCHING FUNC  SATSXXXXB*01`.

Created on 26 Jan 2026

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2026
:license: BSD 3-Clause
"""

from queue import Queue
from sys import argv
from threading import Event, Thread
from time import sleep

from serial import Serial

from pyunigps import NMEA_PROTOCOL, RTCM3_PROTOCOL, UNI_MSGIDS, UNI_PROTOCOL, UNIReader


def io_data(
    unr: UNIReader,
    readqueue: Queue,
    sendqueue: Queue,
    stop: Event,
):
    """
    THREADED
    Read and parse inbound UNI data and place
    raw and parsed data on queue.

    Send any queued outbound messages to receiver.
    """
    # pylint: disable=broad-exception-caught

    while not stop.is_set():
        try:
            raw_data, parsed_data = unr.read()
            if parsed_data:
                readqueue.put((raw_data, parsed_data))

            # refine this if outbound message rates exceed inbound
            while not sendqueue.empty():
                data = sendqueue.get(False)
                if data is not None:
                    unr.datastream.write(data)
                sendqueue.task_done()

        except Exception as err:
            print(f"\n\nSomething went wrong - {err}\n\n")
            continue


def process_data(queue: Queue, stop: Event):
    """
    THREADED
    Get UNI data from queue and display.
    """

    while not stop.is_set():
        if queue.empty() is False:
            _, parsed = queue.get()
            print(parsed)
            queue.task_done()


def send_command(msg: str, queue: Queue):
    """
    Send ASCII configuration command to receiver.
    """

    msgb = f"{msg}\r\n".encode("ascii", errors="backslashreplace")
    print(f"Sending command {msg=}")
    queue.put(msgb)


def main(**kwargs):
    """
    Main routine.
    """

    port = kwargs.get("port", "/dev/ttyACM0")
    baudrate = int(kwargs.get("baudrate", 38400))
    timeout = float(kwargs.get("timeout", 0.1))
    protfilter = int(
        kwargs.get("protfilter", NMEA_PROTOCOL | UNI_PROTOCOL | RTCM3_PROTOCOL)
    )
    sysport = kwargs.get("sysport", "COM1")
    enable = int(kwargs.get("enable", 1))
    read_queue = Queue()
    send_queue = Queue()
    stop_event = Event()

    with Serial(port, baudrate, timeout=timeout) as stream:
        unireader = UNIReader(stream, protfilter=protfilter)
        stop_event.clear()
        io_thread = Thread(
            target=io_data,
            args=(
                unireader,
                read_queue,
                send_queue,
                stop_event,
            ),
            daemon=True,
        )
        process_thread = Thread(
            target=process_data,
            args=(
                read_queue,
                stop_event,
            ),
            daemon=True,
        )

        print("\nStarting handler threads. Press Ctrl-C to terminate...")
        io_thread.start()
        process_thread.start()

        # loop until user presses Ctrl-C
        while not stop_event.is_set():
            try:
                # DO STUFF IN THE BACKGROUND e.g.
                # Enable all available binary UNI data output types
                # on COM1 at a rate of 1Hz.
                # To disable messages, use the `unlog` command e.g.
                # `unlog COM1 SATSINFOB`.
                #
                # You may see a number of `Unknown protocol header b'$c'.`
                # messages in the output - these are simply the ASCII
                # command acknowledgements from the receiver.
                #
                # NB: you may need to apply `config COM1 460800` first to ensure
                # output buffer can handle this volume of output messages, e.g.
                # msg = f"config {sysport} 460800"
                # send_command(msg, send_queue)
                count = 0
                for msg in UNI_MSGIDS.values():
                    if enable:
                        msg = f"{msg}B {sysport} 1"
                    else:
                        msg = f"unlog {sysport} {msg}B"
                    send_command(msg, send_queue)
                    count += 1
                    sleep(0.2)
                stop_event.set()
                print(f"{count} ASCII commands sent to receiver.")

            except KeyboardInterrupt:  # capture Ctrl-C
                print("\n\nTerminated by user.")
                stop_event.set()

        print("\nStop signal set. Waiting for threads to complete...")
        io_thread.join()
        process_thread.join()
        print("\nProcessing complete")


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
