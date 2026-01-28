"""
Created on 6 Oct 2025

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2020
:license: BSD 3-Clause
"""

from pynmeagps import SocketWrapper

from pyunigps._version import __version__
from pyunigps.exceptions import (
    GNSSStreamError,
    ParameterError,
    UNIMessageError,
    UNIParseError,
    UNIStreamError,
    UNITypeError,
)
from pyunigps.unihelpers import *
from pyunigps.unimessage import UNIMessage
from pyunigps.unireader import UNIReader
from pyunigps.unitypes_core import *
from pyunigps.unitypes_get import *

version = __version__  # pylint: disable=invalid-name
