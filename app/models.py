from sqlalchemy import Column, String, Integer, Boolean, ForeignKey  # Columns settings
from sqlalchemy.sql.sqltypes import TIMESTAMP  # for automatically adding local time
from sqlalchemy.sql.expression import text

from app.db.database import Base  # Class to create table


# Users table
class User(Base):
    __tablename__ = 'users'  # just tablename

    id_user: int = Column(Integer, primary_key=True, nullable=False)
    login: str = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False)
    admin: bool = Column(Boolean, server_default=text('False'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# Scores table
class Score(Base):
    __tablename__ = 'scores'

    id_score: int = Column(Integer, primary_key=True, nullable=False)
    id_user: int = Column(Integer, ForeignKey('users.id_user', ondelete='CASCADE'), nullable=False)
    score: int = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

