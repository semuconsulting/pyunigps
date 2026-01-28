---
name: pyunigps Bug Report

about: Create a report to help us improve

title: ''

labels: ''

assignees: semuadmin

---

**Describe the bug**

A clear and concise description of what the bug is. Please include:

1. The pyunigps version (`>>> pyunigps.version`)
2. The **complete** Python script. Embed your code here (please do *NOT* attach *.py, *.zip, *.tgz or other executable / zipped files) ...
   ```python
   your code here
   ```
3. The error message and full traceback.
4. A binary / hexadecimal dump of the UNI data stream.

**To Reproduce**

Steps to reproduce the behaviour:
1. Any relevant device configuration (if other than factory defaults).
2. Any causal UNI command input(s).

**Expected Behaviour**

A clear and concise description of what you expected to happen.

**Desktop (please complete the following information):**

- The operating system you're using [e.g. Windows 11, MacOS Sequoia, Ubuntu Noble].
- The type of serial connection [e.g. USB, UART1, I2C].

**GNSS/GPS Device (please complete the following information as best you can):**

- Device Model/Generation: [e.g. Quectel NEO-9M].
- Firmware Version: [e.g. SPG 4.03].
- Protocol: [e.g. 32.00].
 
This information is typically output by the device at startup via a series of NMEA TXT messages. It can also be found by polling the device with a UNI MON-VER message. If you're using the PyGPSClient GUI, a screenshot of the UNIConfig window should suffice.

**Additional context**

Add any other context about the problem here.
