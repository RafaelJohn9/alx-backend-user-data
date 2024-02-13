#!/usr/bin/env python3
"""
a module that contains class BasicAuth
it inherits from Auth
"""
from api.v1.auth.auth import Auth
import base64


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
                                           base64_authorization_header: str) -> str:
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
