#!/usr/bin/env python3
"""
takes in a password str argument
and return bytes The returned bytes
is a salted hash of the password with bcrypt.hashpw
"""
import bcrypt
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from db import DB
import uuid
from user import User


def _hash_password(password: str) -> str:
    """
    hashes user password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def _generate_uuid() -> str:
    """
    generates a uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        it is used to declare its own attributes
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        authorizes login for user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password.encode('utf-8'))

    def create_session(self, email: str) -> str:
        """
        creates a session id as a string
        """
        if email is None:
            return None

        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            if user:
                self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            return None
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        gets the user through a session id
        """
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """ updates the corresponding user's session ID to none """
        self._db.update_user(user_id, session_id=None)
