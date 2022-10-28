from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from database import get_db
from oauth2 import get_current_user
from repository import playlist as playlist_repository
from schemas import playlist as playlist_schema

router = APIRouter(
    prefix="/playlist",
    tags=["playlists"],
)


@router.post('/', status_code=status.HTTP_202_ACCEPTED)
def add_track_to_user_playlist(
        request: playlist_schema.Playlist,
        db: Session = Depends(get_db),
        current_user_id: int = Depends(get_current_user)
):
    return playlist_repository.add(current_user_id, request, db)


@router.get('/', status_code=status.HTTP_200_OK)
def get_user_playlist(
        db: Session = Depends(get_db),
        current_user_id: int = Depends(get_current_user)
):
    return playlist_repository.get(current_user_id, db)
