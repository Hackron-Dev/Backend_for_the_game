from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.utils.constants import Connection  # Use this class for taking db's URL from .env file


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# URL for connection to db
SQLALCHEMY_DATABASE_URL = f'postgresql://{Connection.SQLALCHEMY_DATABASE_URL}'

# Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()
