from deta import _Base
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import jwtoken
from database import get_users_db
from hashing import Hash

router = APIRouter(
    prefix="/login",
    tags=["auth"],
)


@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), users_db: _Base = Depends(get_users_db)):
    user = users_db.fetch({
        'username': request.username
    }).items

    if len(user) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect username or password")
    user = user[0]
    if not Hash.verify(user['password'], request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect username or password")

    access_token = jwtoken.create_access_token(data={"sub": str(user["username"])})
    return {"access_token": access_token, "token_type": "bearer"}
