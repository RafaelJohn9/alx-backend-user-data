#!/usr/bin/env python3
"""
Personal data - returns the log message obfuscated
"""
import logging
import re
from typing import List
import mysql.connector
import os


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


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    logger of user_data
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(fields=PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    gets the database using the specified environ var
    """
    db_username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    # connecting to the MYSQL database
    connection = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
            )
    return connection


def main():
    """
    this is the main function
    used to output the users info in formatted form
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    fields = ["name",
              "email",
              "phone",
              "ssn",
              "password"
              ]
    logger = get_logger()

    for row in cursor:
        filtered_row = filter_datum(fields,
                                    '***',
                                    row,
                                    ';'
                                    )
        logger.info(str(filtered_row))

    cursor.close()
    db.close()
