"""
unipoller.py

This example illustrates how to read, write and display UNI messages
"concurrently" using threads and queues. This represents a useful
generic pattern for many end user applications.

Usage:

python3 unipoller.py port="/dev/ttyACM0" baudrate=38400 timeout=0.1 protfilter=2

It implements two threads which run concurrently:
1) an I/O thread which continuously reads UNI data from the
receiver and sends any queued outbound ASCII commands.
2) a process thread which processes parsed UNI data - in this example
it simply prints the parsed data to the terminal.
UNI data is passed between threads using queues.

Press CTRL-C to terminate.

FYI: Since Python implements a Global Interpreter Lock (GIL),
threads are not strictly concurrent, though this is of minor
practical consequence here.

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

from pyunigps import NMEA_PROTOCOL, RTCM3_PROTOCOL, UNI_PROTOCOL, UNIReader


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
                # DO STUFF IN THE BACKGROUND...
                # enable a selection of UNI protocol messages on COM1 at a rate of 1Hz...
                count = 0
                rate = 1 # set to 0 to disable UNI messages
                for msg in (
                    "SATSINFO",
                    "OBVSM",
                    "AGRIC",
                    "GPSUTC",
                    "PVTSLN",
                    "HWSTATUS",
                ):
                    # create ASCII TTY message
                    msg = f"{msg}B COM1 {rate}\r\n".encode(
                        "ascii", errors="backslashreplace"
                    )
                    send_queue.put(msg)
                    count += 1
                    sleep(1)
                # stop_event.set()
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
