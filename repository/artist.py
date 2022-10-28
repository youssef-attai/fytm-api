from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import artist as artist_model
from schemas import artist as artist_schema


def create(artist: artist_schema.Artist, db: Session = Depends(get_db)):
    already_exists = db.query(artist_model.Artist).filter(artist_model.Artist.name == artist.name).first()
    if already_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Artist \"{artist.name}\" already exists"
        )

    new_artist = artist_model.Artist(
        name=artist.name
    )

    db.add(new_artist)
    db.commit()
    db.refresh(new_artist)

    return artist_schema.ShowArtist(
        artist_id=new_artist.id,
        name=new_artist.name
    )
