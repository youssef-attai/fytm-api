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
