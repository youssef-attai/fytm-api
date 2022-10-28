from sqlalchemy import Column, Integer, ForeignKey

import models.track
import models.user
from database import Base


class Playlist(Base):
    __tablename__ = 'playlists'

    user_id = Column(Integer, ForeignKey(models.user.User.id), primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey(models.track.Track.id), primary_key=True, index=True)