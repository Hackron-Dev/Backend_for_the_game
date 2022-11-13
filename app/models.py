from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from app.db.database import Base


class User(Base):
    __tablename__ = 'users'

    id_user: int = Column(Integer, primary_key=True, nullable=False)
    login: str = Column(String, nullable=False)
    password: str = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Score(Base):
    __tablename__ = 'scores'

    id_score: int = Column(Integer, primary_key=True, nullable=False)
    id_user: int = Column(Integer, ForeignKey('users.id_user', ondelete='CASCADE'), nullable=False)
    score: int = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

