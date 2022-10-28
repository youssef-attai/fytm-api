from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repository import user as user_repository
from schemas import user as user_schemas

router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.post('/', response_model=user_schemas.ShowUser)
def create_user(request: user_schemas.User, db: Session = Depends(get_db)):
    return user_repository.create(request, db)


@router.get('/{uid}', response_model=user_schemas.ShowUser)
def get_user_by_id(uid: int, db: Session = Depends(get_db)):
    return user_repository.get_by_id(uid, db)
