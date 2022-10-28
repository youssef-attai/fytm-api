from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import playlist as playlist_model
from schemas import playlist as playlist_schema


def add(
        uid: int,
        playlist: playlist_schema.Playlist,
        db: Session = Depends(get_db)
):
    new_user_track_pair = playlist_model.Playlist(
        user_id=uid,
        track_id=playlist.track_id
    )
    db.add(new_user_track_pair)
    db.commit()
    db.refresh(new_user_track_pair)
    return new_user_track_pair


def get(uid: int, db: Session = Depends(get_db)):
    return db.query(playlist_model.Playlist).filter(playlist_model.Playlist.user_id == uid).all()
