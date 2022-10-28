from sqlalchemy import Column, Integer, String, ForeignKey

import models.album
import models.artist
from database import Base


class Track(Base):
    __tablename__ = 'tracks'

    # TODO: track ID is the YouTube video ID
    id = Column(Integer, primary_key=True, index=True)
    youtube = Column(String)

    title = Column(String)
    year = Column(Integer)
    artist = Column(Integer, ForeignKey(models.artist.Artist.id))  # Artist ID
    album = Column(Integer, ForeignKey(models.album.Album.id))  # Album ID
    audio_url = Column(String)
