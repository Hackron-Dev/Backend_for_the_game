from fastapi import FastAPI

from app.routers import user, scores

app = FastAPI()

app.include_router(user.router)
app.include_router(scores.router)


@app.get("/")
def main_page():
    return {"Hello": "world"}
