#!/usr/bin/env python3
"""the class Auth"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """class named Auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        for excluded_path in excluded_paths:
            stripped = excluded_path.rstrip('*')
            if path.startswith(stripped):
                return False
        if path in excluded_paths or path + '/' in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """that returns None - request will be the Flask request object"""
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """that returns None - request will be the Flask request object"""
        return None
