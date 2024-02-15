#!/usr/bin/env python3
"""BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic authentication
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Authorization header for a Basic Authentication
        """
        if not authorization_header or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """the decoded value of a Base64 string base64_authorization_header"""
        header = base64_authorization_header

        if not header or type(header) is not str:
            return None

        try:
            code = base64.b64decode(base64_authorization_header)
            return code.decode('utf-8')

        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """the user email and password from the Base64 decoded value."""
        decoded_header = decoded_base64_authorization_header

        if not decoded_header or type(decoded_header) is not str:
            return (None, None)

        if ":" not in decoded_header:
            return (None, None)
        details = decoded_header.split(':')
        return (details[0], details[1])

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None
        try:
            user = User.search({'email': user_email})
            if not len(user):
                return (None)
            if not user[0].is_valid_password(user_pwd):
                return (None)
            return (user[0])
        except Exception:
            return (None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth and retrieves the User instance for a request """
        auth = self.authorization_header(request)
        extract = self.extract_base64_authorization_header(auth)
        decode = self.decode_base64_authorization_header(extract)
        email, pwd = self.extract_user_credentials(decode)
        return (self.user_object_from_credentials(email, pwd))
