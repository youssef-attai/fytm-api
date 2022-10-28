from pydantic import BaseModel


class Album(BaseModel):
    name: str
    artist: int
