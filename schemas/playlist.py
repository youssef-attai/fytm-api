from pydantic import BaseModel


class Playlist(BaseModel):
    track_id: str


class ShowPlaylist(BaseModel):
    username: str
    track_title: str
