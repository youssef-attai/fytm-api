from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import track as track_model
from schemas import track as track_schema


def create(track: track_schema.Track, db: Session = Depends(get_db)):
    new_track = track_model.Track(
        title=track.title,
        year=track.year,
        artist=track.artist,
        album=track.album,
        youtube=track.youtube,
        audio_url=track.audio_url
    )
    db.add(new_track)
    db.commit()
    db.refresh(new_track)
    return new_track
