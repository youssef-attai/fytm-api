from fastapi import APIRouter, Depends

from schemas import user as user_schemas
from repository import user as user_repository
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.post('/', response_model=user_schemas.ShowUser)
def create_user(request: user_schemas.User, db: Session = Depends(get_db)):
    return user_repository.create(request, db)


@router.get('/{id}', response_model=user_schemas.ShowUser)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return user_repository.get_by_id(id, db)
