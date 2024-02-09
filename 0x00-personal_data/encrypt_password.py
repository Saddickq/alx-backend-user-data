#!/usr/bin/env python3
"""
bcrypt file
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    a hash_password function that expects one
    string argument name password and returns
    a salted, hashed password, which is a byte string.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
