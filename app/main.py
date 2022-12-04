from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response

from app.routers import users, shop, auth, admin
from app.db.database import init_db

app = FastAPI(title="Using Tortoise")

app.include_router(users.router)
app.include_router(users.user_router)
app.include_router(shop.router)
app.include_router(auth.router)
app.include_router(admin.router)


@app.on_event("startup")  # before starting creating database
async def startup_event():
    init_db(app)


@app.get("/", include_in_schema=False)
async def info(request: Request) -> Response:
    # Use 302 (Temporary redirect) to avoid browsers to cache this
    # since the API may at some point actually have some index page
    # rather than just always redirecting to docs page
    # return Response("hello")
    return RedirectResponse(url="/docs", status_code=302)
