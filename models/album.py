from sqlalchemy import Column, Integer, String, ForeignKey

import models.artist
from database import Base


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    artist = Column(Integer, ForeignKey(models.artist.Artist.id))
