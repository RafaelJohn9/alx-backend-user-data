#!/usr/bin/env python3
"""
Personal data - returns the log message obfuscated
"""
from typing import List
import re
import logging


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        contain object attr
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        correctly formats user's data
        """
        for field in self.fields:
            record.msg = re.sub(fr'({field})=([^;]+)',
                                fr'\1={self.REDACTION}',
                                record.msg)
        return super().format(record)


PII_FIELDS = ("name", "email", "phone", "ssn", "credit_card")


def get_logger() -> logging.Logger:
    """
    logger of user_data
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(fields=PII_FIELDS)

    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger
