from fastapi import Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from database import get_db
from models import playlist as playlist_model
from models import track as track_model
from models import user as user_model
from schemas import playlist as playlist_schema


def add(
        uid: int,
        playlist: playlist_schema.Playlist,
        db: Session = Depends(get_db)
):
    the_user = db.query(user_model.User).filter(user_model.User.id == uid).first()
    if the_user is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f'User with ID {uid} is not found'
        )

    the_track = db.query(track_model.Track).filter(track_model.Track.id == playlist.track_id).first()
    if the_track is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Track with ID {playlist.track_id} is not found'
        )

    already_exists = db.query(playlist_model.Playlist).filter(
        and_(
            playlist_model.Playlist.user_id == uid,
            playlist_model.Playlist.track_id == playlist.track_id
        )
    ).first()

    if already_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Track \"{the_track.title}\" is already added to {the_user.username}'s playlist"
        )

    new_user_track_pair = playlist_model.Playlist(
        user_id=uid,
        track_id=playlist.track_id
    )

    db.add(new_user_track_pair)
    db.commit()
    db.refresh(new_user_track_pair)

    return playlist_schema.ShowPlaylist(
        username=the_user.username,
        track_title=the_track.title
    )


def get(uid: int, db: Session = Depends(get_db)):
    the_user = db.query(user_model.User).filter(user_model.User.id == uid).first()
    if the_user is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f'User with ID {uid} does not exist'
        )

    return db.query(playlist_model.Playlist).filter(playlist_model.Playlist.user_id == uid).all()
