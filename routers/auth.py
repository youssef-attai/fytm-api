from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from schemas import login as login_schema
from models import user as user_model
from sqlalchemy.orm import Session
from hashing import Hash
import jwtoken 
# from blog import schemas, database, models, token
# from blog.hashing import Hash

router = APIRouter(
    prefix="/login",
    tags=["auth"],
)


@router.post('/')
def login(request: login_schema.Login = Depends(), db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(
        user_model.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = jwtoken.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}