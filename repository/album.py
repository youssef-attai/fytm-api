from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import album as album_model
from schemas import album as album_schema


def create(album: album_schema.Album, db: Session = Depends(get_db)):
    new_album = album_model.Album(
        name=album.name,
        artist=album.artist
    )
    db.add(new_album)
    db.commit()
    db.refresh(new_album)
    return new_album
