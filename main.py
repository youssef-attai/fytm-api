import re
import urllib.request

from deta import _Base
from fastapi import FastAPI, Depends, HTTPException, status
from pytube import YouTube
import schemas.track
import schemas.user
from database import get_users_db
from hashing import Hash
from oauth2 import get_current_user
from routers import auth as auth_router

app = FastAPI()

app.include_router(auth_router.router)


def youtube_url(watch_id):
    return f'https://youtube.com/watch?v={watch_id}'


def create_track_from_watch_id(watch_id):
    yt = YouTube(youtube_url(watch_id))
    title = yt.title
    author = yt.author
    thumbnail_url = yt.thumbnail_url

    return schemas.track.Track(
        title=title,
        author=author,
        thumbnail_url=thumbnail_url
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
    html_page = urllib.request.urlopen(f'https://youtube.com/results?search_query={q}')
    videos_watch_ids = re.findall(r'watch\?v=(\S{11})', html_page.read().decode())
    return videos_watch_ids


@app.get('/track/{watch_id}')
async def track(watch_id: str):
    return create_track_from_watch_id(watch_id)


@app.get('/audio/{watch_id}')
async def audio(watch_id: str):
    yt = YouTube(youtube_url(watch_id))
    return yt.streams.get_audio_only().url


@app.get('/whoami')
async def whoami(current_username: str = Depends(get_current_user)):
    return current_username
