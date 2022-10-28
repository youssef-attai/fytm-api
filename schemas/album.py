from pydantic import BaseModel


class Album(BaseModel):
    name: str
    artist: int


class ShowAlbum(BaseModel):
    album_id: int
    name: str
    artist: str
