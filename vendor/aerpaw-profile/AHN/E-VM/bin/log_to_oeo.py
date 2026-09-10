#!/usr/bin/env python3
import sys

from aerpawlib import AERPAW_Platform

if len(sys.argv) < 3:
    print("Usage: log_to_oeo.py <LEVEL> <MESSAGE>")
    sys.exit(1)

level = sys.argv[1]
message = " ".join(sys.argv[2:])
AERPAW_Platform.log_to_oeo(message, level)
