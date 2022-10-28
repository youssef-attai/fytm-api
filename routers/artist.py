from fastapi import APIRouter, status
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from repository import artist as artist_repository
from schemas import artist as artist_schema

router = APIRouter(
    prefix="/artist",
    tags=["artists"],
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_artist(
        request: artist_schema.Artist,
        db: Session = Depends(get_db),
        # current_user_id: int = Depends(get_current_user)
):
    return artist_repository.create(request, db)
