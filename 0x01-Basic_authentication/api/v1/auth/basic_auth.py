#!/usr/bin/env python3
"""BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64


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
