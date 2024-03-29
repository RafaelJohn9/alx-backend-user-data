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
        it used to check if a certain path requires authorization
        """
        if not path or not excluded_paths:
            return True

        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            stripped = excluded_path.rstrip('*')
            if path.startswith(stripped):
                return False

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        used for authorization header
        """
        if not request or not request.headers.get("Authorization"):
            return None
        else:
            return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None request
        """
        return None
