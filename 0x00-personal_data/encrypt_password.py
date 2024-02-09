#!/usr/bin/env python3
"""
bcrypt file
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    encrypt password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password) -> bool:
    """
    validate password
    """
    return bcrypt.checkpw(bytes(password, "utf-8"), hashed_password)
