"""
unitypes_decodes.py

UNI Protocol decodes and enumerations.

Created on 26 Jan 2026

Information sourced from public domain Unicore Reference Commands R1.13 © Dec 2025 Unicore
https://en.unicore.com/uploads/file/Unicore%20Reference%20Commands%20Manual%20For%20N4%20High%20Precision%20Products_V2_EN_R1.13.pdf

:author: semuadmin (Steve Smith)
"""

DEVICE = {
    0: "UNKNOWN",
    1: "UB4B0",
    2: "UM4B0",
    3: "UM480",
    4: "UM440",
    5: "UM482",
    6: "UM442",
    7: "UB482",
    8: "UT4B0",
    10: "UB362L",
    11: "UB4B0M",
    12: "UB4B0J",
    13: "UM482L",
    14: "UM4B0L",
    16: "CLAP-B",
    17: "UM982",
    18: "UM980",
    19: "UM960",
    21: "UM980A",
    23: "CLAP-C",
    24: "UM960L",
    26: "UM981",
    31: "UM981S",
    40: "UMD982",
    41: "UMD981",
    42: "UMD981S",
    43: "UM981C",
    52: "UB9A0",
    53: "UBD9A0",
    62: "UMD960",
    63: "UMD980",
    64: "UM980C",
    65: "UM982C",
}
"""Hardware Device Code"""

GNSS = {
    0: "GPS",
    1: "GLONASS",
    2: "SBAS",
    3: "GAL",
    4: "BDS",
    5: "QZSS",
    6: "IRNSS",
    7: "Reserved",
}
"""SATSINFO GNSS Satellite System Code"""

GNSSSAT = {
    0: "GPS",
    1: "GLONASS",
    2: "SBAS",
    5: "GAL",
    6: "BDS",
    7: "QZSS",
    9: "IRNSS",
}
"""SATELLITE GNSS Satellite System Code"""

CALCSTATUS = {
    0: "No differential data input",
    1: "Insufficient observation at the differential source",
    2: "High latency of differential data",
    3: "Active ionosphere (valid for base station mode)",
    4: "Insufficient observation at the ROVER",
    5: "RTK solution available",
}
"""RTK Calculate Status"""

POSTYPE = {
    0: "NONE",  # No solution
    1: "FIXEDPOS",  #  Position fixed by the FIX POSITION command
    2: "FIXEDHEIGHT",  #  Not supported currently
    8: "DOPPLER_VELOCITY",  #  Velocity computed using instantaneous Doppler
    16: "SINGLE",  #  Single point positioning
    17: "PSRDIFF",  #  Pseudorange differential solution
    18: "SBAS",  #  SBAS positioning
    32: "L1_FLOAT L1",  #  float solution
    33: "IONOFREE_FLOAT",  #  Ionosphere-free float solution
    34: "NARROW_FLOAT",  #  Narrow-lane float solution
    48: "L1_INT",  #  L1 fixed solution
    49: "WIDE_INT",  #  Wide-lane fixed solution
    50: "NARROW_INT",  #  Narrow-lane fixed solution
    52: "INS",  #  Inertial navigation solution
    53: "INS_PSRSP",  #  Integrated solution of INS and single point positioning
    54: "INS_PSRDIFF",  #  Integrated solution of INS and pseudorange differential positioning
    55: "INS_RTKFLOAT",  #  Integrated solution of INS and RTK float
    56: "INS_RTKFIXED",  #  Integrated solution of INS and RTK fix
    68: "PPP_CONVERGING",  #  PPP solution converging
    69: "PPP",  #  Precise Point Positioning
}
"""Position/Velocity Type"""

SOLSTATUS = {
    0: "SOL_COMPUTED",  # Solution computed
    1: "INSUFFICIENT_OBS",  # Insufficient observation
    2: "NO_CONVERGENCE",  # No convergence, invalid solution
    4: "COV_TRACE",  # Covariance matrix trace exceeds maximum (trace > 1000 m)
}
"""Solution Status"""

ROVERPOSTYPE = {
    0: "Invalid",
    1: "Single point",
    2: "Pseudorange differential",
    4: "Fixed",
    5: "Float",
    7: "Input a fixed position",
}
""" Rover Position Status"""

PSRSTD = {
    0: 0.050,
    1: 0.075,
    2: 0.113,
    3: 0.169,
    4: 0.253,
    5: 0.380,
    6: 0.570,
    7: 0.854,
    8: 1.281,
    9: 2.375,
    10: 4.750,
    11: 9.500,
    12: 19.000,
    13: 38.000,
    14: 76.000,
    15: 152.000,
}
"""OBSVMCMP Pseudorange Standard Deviation Lookup"""

PSRIONOCORR = {
    0: "Unknown",
    1: "Klobuchareph",
    2: "SBASionogrid",
    3: "Multifreq",
    4: "Psrdiff",
}
"""EXTSOLSTAT Pseudorange Ionospheric Correction"""

BD3EPH_FREQTYPE = {
    0: "B1C",
    1: "B2a",
    2: "B2b",
}
"""BD3EPH Frequency Type"""

GLOEPH_SATTYPE = {
    0: "GLO_SAT",
    1: "GLO_SAT_M",
    2: "GLO_SAT_K",
}
"""GLOEPH Satellite Type"""
