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

    return user_schema.ShowUser(
        username=new_user.username
    )


def get_by_id(uid: int, db: Session = Depends(get_db)):
    the_user = db.query(user_model.User).filter(user_model.User.id == uid).first()
    if the_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {uid} does not exist"
        )

    return user_schema.ShowUser(
        username=the_user.username
    )
