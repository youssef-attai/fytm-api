from fastapi import Depends, HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from database import get_db
from models import album as album_model
from models import artist as artist_model
from schemas import album as album_schema


def create(album: album_schema.Album, db: Session = Depends(get_db)):
    the_artist = db.query(artist_model.Artist).filter(artist_model.Artist.id == album.artist).first()
    if the_artist is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f'Artist with ID {album.artist} is not found.')

    new_album = album_model.Album(
        name=album.name,
        artist=album.artist
    )

    db.add(new_album)
    db.commit()
    db.refresh(new_album)

    return album_schema.ShowAlbum(
        album_id=new_album.id,
        name=new_album.name,
        artist=the_artist.name
    )


def search(
        query: str,
        db: Session = Depends(get_db)
):
    results = db.query(album_model.Album, artist_model.Artist).filter(
        album_model.Album.artist == artist_model.Artist.id
    ).filter(
        album_model.Album.name.ilike(f"%{query}%")
    ).all()

    return [album_schema.ShowAlbum(
        album_id=res.Album.id,
        name=res.Album.name,
        artist=res.Artist.name
    ) for res in results]


def by(
        artist_id: int,
        db: Session = Depends(get_db)
):
    results = db.query(album_model.Album, artist_model.Artist).filter(
        and_(
            album_model.Album.artist == artist_model.Artist.id,
            album_model.Album.artist == artist_id
        )
    ).all()

    return [album_schema.ShowAlbum(
        album_id=res.Album.id,
        name=res.Album.name,
        artist=res.Artist.name
    ) for res in results]
