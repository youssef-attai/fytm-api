from pydantic import BaseModel


class Playlist(BaseModel):
    # user_id: int
    track_id: int
