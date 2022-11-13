# Create backend for the game 
___
### Using Fastapi
___
### settings for usage
`pip install -r requirements.txt`

create `.evn` file and ADD `SQLALCHEMY_DATABASE_URL` 

mask `SQLALCHEMY_DATABASE_URL="{username}:{password}@{hostname}:{port}/{db_name}"`

example `SQLALCHEMY_DATABASE_URL="postgres:0030@localhost:5432/gamefor"`

### for running use pycharm or command 
`uvicorn app.main:app --host=localhost --port=8080`
