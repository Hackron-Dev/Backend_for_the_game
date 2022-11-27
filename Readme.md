# Create backend for the game 
 Using Fastapi
# Setup settings before run
```shell
> pip install -r requirements.txt
```

Create `.evn` File and ADD `DATABASE_URL`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `ALGORITHM` 

Mask

```python
DATABASE_URL="{username}:{password}@{hostname}:{port}/{db_name}"
```

Example: 
```python
DATABASE_URL="postgres:0030@localhost:5432/gamefor" # your db url
SECRET_KEY="dfj;alsjiur20r0jsdjfsdlkmflsdjoid" # any symbols what you wont
ACCESS_TOKEN_EXPIRE_MINUTES=60 # how many do you wont use token
ALGORITHM="HS256" # Use this by default
```

for run use Pycharm or with command on terminal
```shell
> uvicorn app.main:app --host=localhost --port=8080
```

# Migration with `aerich`
Inti DB for starting migrations
```shell
> aerich init-db
```
For migrating changes
```shell
> aerich migrate --name TEXT  Migrate name.  [default: update]
```
Upgrade to specified version.
```shell
> aerich upgrade
```
# Project Contributors
<a href="https://github.com/Hackron-Dev/Backend_for_the_game/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=Hackron-dev/Backend_for_the_game">
</a>
