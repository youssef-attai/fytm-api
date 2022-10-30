import re
import urllib.request

from deta import Deta
from fastapi import FastAPI
from pydantic import BaseModel
from pytube import YouTube

app = FastAPI()

deta = Deta()
db = deta.Base(name='users')


class Track(BaseModel):
    title: str
    author: str
    thumbnail_url: str


def youtube_url(watch_id):
    return f'https://youtube.com/watch?v={watch_id}'


def create_track_from_watch_id(watch_id):
    yt = YouTube(youtube_url(watch_id))
    title = yt.title
    author = yt.author
    thumbnail_url = yt.thumbnail_url

    return Track(
        title=title,
        author=author,
        thumbnail_url=thumbnail_url
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
