import asyncio
import re
import urllib.request

from deta import _Base
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL

import schemas.track
import schemas.user
from database import get_users_db
from hashing import Hash
from oauth2 import get_current_user
from routers import auth as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)


def youtube_url(watch_id):
    return f'https://youtube.com/watch?v={watch_id}'


def create_track_from_watch_id(watch_id):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url(watch_id), download=False)

    return schemas.track.Track(
        watch_id=info["id"],
        title=info["title"],
        author=info["channel"],
        thumbnail_url=info["thumbnail"],
        audio_url=info["url"]
    )


@app.post('/user')
async def create_user(request: schemas.user.User, users_db: _Base = Depends(get_users_db)):
    user_exists = users_db.fetch({
        'username': request.username
    }).items

    if len(user_exists) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Username "{request.username}" already exists'
        )

    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Password should be at least 8 characters long'
        )

    user = users_db.insert({
        "username": request.username,
        "password": Hash.bcrypt(request.password)
    })

    return schemas.user.ShowUser(
        username=user['username'],
        key=user['key']
    )


@app.get('/search')
async def search(q: str = ''):
    q = '+'.join(q.split())
    html_page = urllib.request.urlopen(f'https://youtube.com/results?search_query={q}')
    videos_watch_ids = re.findall(r'watch\?v=(\S{11})', html_page.read().decode())[:10]
    return await asyncio.gather(
        *[asyncio.to_thread(lambda wa=w: create_track_from_watch_id(wa)) for w in set(videos_watch_ids)]
    )


# @app.get('/track/{watch_id}')
# async def track(watch_id: str):
#     return create_track_from_watch_id(watch_id)


@app.get('/audio/{watch_id}')
async def audio(watch_id: str):
    return f'audio for {watch_id}'
    # yt = YouTube(youtube_url(watch_id))
    # return yt.streams.get_audio_only().url


@app.get('/whoami')
async def whoami(current_username: str = Depends(get_current_user)):
    return current_username
