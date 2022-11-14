from fastapi import FastAPI

from app import models
from app.db.database import engine
from app.routers import user, scores

# for create table on db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# two router for two url paths
app.include_router(user.router)  # users router
app.include_router(scores.router)  # scores router


# just for test
@app.get("/")
def main_page():
    return {"Hello": "world"}
