#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4
from db import DB


def _generate_uuid() -> str:
    """generate unique id"""
    return str(uuid4())


def _hash_password(password: str) -> bytes:
    """Generate hashed password"""
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """ validate credentials"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)
