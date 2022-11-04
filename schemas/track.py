from pydantic import BaseModel

from pydantic.dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Track(BaseModel):
    watch_id: str
    title: str
    author: str
    thumbnail_url: str
    audio_url: str
