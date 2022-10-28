from fastapi import APIRouter, status
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from oauth2 import get_current_user
from repository import album as album_repository
from schemas import album as album_schema
from schemas import user as user_schema

router = APIRouter(
    prefix="/album",
    tags=["albums"],
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_album(
        request: album_schema.Album,
        db: Session = Depends(get_db),
        current_user: user_schema.User = Depends(get_current_user)
):
    return album_repository.create(request, db)
