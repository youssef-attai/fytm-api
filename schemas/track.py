from pydantic import BaseModel


class Track(BaseModel):
    title: str
    year: int
    artist: int
    album: int
    youtube: str

    # TODO: Should be removed from schema and added to Track(Base) instances
    #  via pytube in the track_router
    audio_url: str
