#!/usr/bin/env python3
"""
a module that contains class BasicAuth
it inherits from Auth
"""
from api.v1.auth.auth import Auth


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
