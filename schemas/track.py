from pydantic import BaseModel


class Track(BaseModel):
    title: str
    year: int
    artist: int
    album: int
    youtube: str
    audio_url: str
