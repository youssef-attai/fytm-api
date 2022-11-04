from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import accounts as auth_router
from routers import track as track_router
from routers import favorites as favorites_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(track_router.router)
app.include_router(favorites_router.router)
