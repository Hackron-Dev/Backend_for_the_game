from sqlalchemy import Table, Column, String, Integer

from app.db.database import metadata

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('Login', String, nullable=False),
              Column('Hash_Password', String, nullable=False),
              Column('Score', Integer, default=0))
