#!/usr/bin/env python3
"""
takes in a password str argument
and return bytes The returned bytes
is a salted hash of the password with bcrypt.hashpw
"""
import bcrypt


def _hash_password(password: str) -> str:
    """
    hashes user password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')
