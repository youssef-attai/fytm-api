from fastapi import Depends, HTTPException, status
from database import get_db
from hashing import Hash
from schemas import user as user_schema
from models import user as user_model
from sqlalchemy.orm import Session


def create(request: user_schema.User, db: Session = Depends(get_db)):
    new_user = user_model.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available"
        )
    return user
