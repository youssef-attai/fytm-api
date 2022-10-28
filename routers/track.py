from fastapi import APIRouter, status
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from repository import track as track_repository
from schemas import track as track_schema

router = APIRouter(
    prefix="/track",
    tags=["tracks"],
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_track(
        request: track_schema.Track,
        db: Session = Depends(get_db),
        # current_user_id: int = Depends(get_current_user)
):
    return track_repository.create(request, db)


@router.get('/search', status_code=status.HTTP_200_OK)
def search_tracks(
        query: str = "",
        db: Session = Depends(get_db),
):
    return track_repository.search(query, db)


@router.get('/by/{artist_id}', status_code=status.HTTP_200_OK)
def get_tracks_by_artist(artist_id: int, db: Session = Depends(get_db)):
    return track_repository.by(artist_id, db)


@router.get('/by/{album_id}', status_code=status.HTTP_200_OK)
def get_tracks_in_album(album_id: int, db: Session = Depends(get_db)):
    return track_repository.in_album(album_id, db)
