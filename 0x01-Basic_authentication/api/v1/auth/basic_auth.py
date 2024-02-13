#!/usr/bin/env python3
"""
a module that contains class BasicAuth
it inherits from Auth
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    Basic Auth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str
                                            ) -> str:
        """
        extracts the base64 encoded text from
        authorization header
        """
        parameter_checker = [
                             authorization_header is not None,
                             isinstance(authorization_header, str),
                             authorization_header[:6] == "Basic "
                             if authorization_header and
                             isinstance(authorization_header, str) else False
                             ]
        if False in parameter_checker:
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        returns the decoded base64 string
        """
        parameter_checker = [
                             base64_authorization_header is not None,
                             isinstance(base64_authorization_header, str)
                             ]
        if False in parameter_checker:
            return None

        decoded_value = None
        try:
            decoded_value_bytes = base64.b64decode(base64_authorization_header)
            decoded_value = decoded_value_bytes.decode('utf-8')
        except Exception:
            return None

        return decoded_value

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        used to extract user credentials from decode values
        from base64
        """
        parameter_checker = [
                             decoded_base64_authorization_header is not None,
                             isinstance(decoded_base64_authorization_header,
                                        str),
                             ':' in decoded_base64_authorization_header
                             if decoded_base64_authorization_header and
                             isinstance(decoded_base64_authorization_header,
                                        str)else False
                             ]
        if False in parameter_checker:
            return (None, None)

        credentials = decoded_base64_authorization_header.split(':')
        email = credentials[0]
        password = ':'.join(credentials[1:]) if len(credentials) > 2 else credentials[1]
        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """
        fetches and validates user's credentials
        """
        parameter_checker = [
                             user_email is not None,
                             user_pwd is not None,
                             User.search({'email': user_email}) is not None
                             if isinstance(user_email, str)
                             else False
                             ]
        if False in parameter_checker:
            return None

        try:
            user = User.search({'email': user_email})
            if user:
                if user[0].is_valid_password(user_pwd):
                    return user[0]
        except Exception:
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
