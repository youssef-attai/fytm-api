from pydantic import BaseModel


class Artist(BaseModel):
    name: str


class ShowArtist(BaseModel):
    artist_id: int
    name: str
