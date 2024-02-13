#!/usr/bin/env python3
"""
a module that contains a class that manages API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    it used in authentication of users
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        it used to for validation for authorization
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        used for authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None request
        """
        return None
