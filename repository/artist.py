from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import artist as artist_model
from schemas import artist as artist_schema


def create(artist: artist_schema.Artist, db: Session = Depends(get_db)):
    new_artist = artist_model.Artist(
        name=artist.name
    )
    db.add(new_artist)
    db.commit()
    db.refresh(new_artist)
    return new_artist
