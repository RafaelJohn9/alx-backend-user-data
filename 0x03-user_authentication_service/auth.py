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
     it  generates a uuid when called
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
        """
        it is used to register a new user to the db
        if not yet registered else throws an error
        """
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

    def get_reset_password_token(self,  email: str) -> str:
        """
        it genereates a reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            user.reset_token = reset_token
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(reset_token: str, password: str) -> None:
        """
        it is used to update a user's password from the database
        """
        if not reset_token or not password:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(
                                 user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None
                                 )
        except NoResultFound:
            raise ValueError
