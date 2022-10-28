from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from hashing import Hash
from models import user as user_model
from schemas import user as user_schema


def create(request: user_schema.User, db: Session = Depends(get_db)):
    new_user = user_model.User(
        username=request.username,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_by_id(uid: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id == uid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {uid} is not available"
        )
    return user
