from pydantic import BaseModel


class Track(BaseModel):
    title: str
    author: str
    thumbnail_url: str
