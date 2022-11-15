from sqlalchemy import create_engine, MetaData

engine = create_engine('sqlite:///users.db', echo=True)
metadata = MetaData()
conn = engine.connect()

