from pydantic import BaseModel


class Track(BaseModel):
    youtube: str
    title: str
    artist: int
    album: int


class ShowTrack(BaseModel):
    track_id: str
    title: str
    artist: str
    album: str
