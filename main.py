from fastapi import FastAPI
from routers import user as user_router
from routers import auth as auth_router
from database import engine
from models import user as user_model


app = FastAPI()


user_model.Base.metadata.create_all(engine)

app.include_router(user_router.router)
app.include_router(auth_router.router)
