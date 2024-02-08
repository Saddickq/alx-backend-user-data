#!/usr/bin/env python3
"""
a function called filter_datum that returns the log message obfuscated
"""
import re
import mysql.connector
from os import getenv
import logging
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """init method"""
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """method to filter values in incoming log records using filter_datum.
        Values for fields in fields should be filtered."""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Arguments:
        fields: a list of strings representing all fields to obfuscate

        redaction: a string representing by what the field will be obfuscated

        message: a string representing the log line

        separator: a string representing by which character is separating
            all fields in the log line (message)
    """
    for field in fields:
        message = re.sub(r"{}=(.*?){}".format(field, separator),
                         "{}={}{}".format(field, redaction, separator),
                         message)

    return message


def get_logger() -> logging.Logger:
    """function that takes no arguments"""
    logger = logging.getLogger("user_data")

    strhd = logging.StreamHandler()
    fmt = RedactingFormatter(list(PII_FIELDS))

    strhd.setFormatter(fmt)
    strhd.setLevel(logging.INFO)

    logger.propergate = False
    logger.addHandler(strhd)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """connect to mysql database"""
    db = mysql.connector.connect(
            user=getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
            host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
            password=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
            database=getenv('PERSONAL_DATA_DB_NAME')
            )
    return db
