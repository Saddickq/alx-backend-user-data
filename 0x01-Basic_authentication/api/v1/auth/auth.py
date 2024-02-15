#!/usr/bin/env python3
"""A class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class for authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method"""

        if path and excluded_paths:
            path = path if path.endswith('/') else path + '/'

            if path in excluded_paths:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """public method"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """public method"""
        return None
