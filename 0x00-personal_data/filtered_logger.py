#!/usr/bin/env python3
"""
Personal data - returns the log message obfuscated
"""
from typing import List
import re


def filter_datum(
                 fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    returns the log message obfuscated
    at fields listed
    """
    return re.sub(fr'({"|".join(fields)})=[^{separator}]+',
                  fr'\1={redaction}', message)
