from fastapi import FastAPI
from routers import user as user_router
from routers import auth as auth_router
from routers import track as track_router
from database import engine, Base


app = FastAPI()


Base.metadata.create_all(engine)

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(track_router.router)
