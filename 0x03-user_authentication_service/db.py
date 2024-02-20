#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        adds new user to the database
        """
        session = self._session
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            session.add(new_user)
            session.commit()
            return (new_user)
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    def find_user_by(self, **kwargs):
        """
        finds user through key-word filter
        """
        session = self._session
        table = session.query(User)
        try:
            query = table.filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return query

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        updates a certain value for the user
        """
        session = self.__session
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            else:
                user.key = value
        session.commit()
