from fastapi import Depends, HTTPException, status
from pytube import YouTube
from sqlalchemy.orm import Session

from database import get_db
from models import album as album_model
from models import artist as artist_model
from models import track as track_model
from schemas import track as track_schema


def create(track: track_schema.Track, db: Session = Depends(get_db)):
    track_exists = db.query(track_model.Track).filter(track_model.Track.id == track.youtube).first()
    if track_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'This YouTube track already exists.'
        )

    the_artist = db.query(artist_model.Artist).filter(artist_model.Artist.id == track.artist).first()
    if the_artist is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f'Artist with ID {track.artist} is not found.'
        )

    the_album = db.query(album_model.Album).filter(album_model.Album.id == track.album).first()
    if the_album is None:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=f'Album with ID {track.artist} is not found.'
        )

    yt_audio_only_url = YouTube(
        f'https://www.youtube.com/watch?v={track.youtube}'
    ).streams.get_audio_only().url

    new_track = track_model.Track(
        id=track.youtube,
        title=track.title,
        artist=track.artist,
        album=track.album,
        audio_url=yt_audio_only_url
    )

    db.add(new_track)
    db.commit()
    db.refresh(new_track)

    return track_schema.ShowTrack(
        track_id=new_track.id,
        title=new_track.title,
        artist=the_artist.name,
        album=the_album.name
    )
