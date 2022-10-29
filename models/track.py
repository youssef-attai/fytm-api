from sqlalchemy import Column, Integer, String, ForeignKey

import models.album
import models.artist
from database import Base


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(200))
    artist = Column(Integer, ForeignKey(models.artist.Artist.id))  # Artist ID
    album = Column(Integer, ForeignKey(models.album.Album.id))  # Album ID
    audio_url = Column(String(500))
