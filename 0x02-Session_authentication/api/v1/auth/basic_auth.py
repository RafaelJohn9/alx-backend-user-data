#!/usr/bin/env python3
"""the class basic_auth"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns the Base64 part of the Authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ returns the decoded value of a Base64 string """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """returns the user email and password"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and pass"""
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        try:
            user = User.search({"email": user_email})
            if user:
                pwd = user[0].is_valid_password(user_pwd)
                if pwd:
                    return user[0]
            return None
        except KeyError:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance"""
        if request is None:
            return None
        authorization_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
            authorization_header)
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header)

        return self.user_object_from_credentials(user_email, user_pwd)
