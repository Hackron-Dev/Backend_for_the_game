from sqlalchemy import Table, Column, String, Integer

from app.db.database import Base


class Users(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, nullable=False)
    login: str = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False)
    mcoin: int = Column(Integer, default=0)
    rcoin: int = Column(Integer, default=0)
