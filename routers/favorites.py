from deta import _Base
from fastapi import Depends, APIRouter, HTTPException, status

import schemas.track
from database import get_favorites_db
from oauth2 import get_current_user

router = APIRouter(
    prefix="/favorite",
    tags=["favorite"],
)


@router.get('/')
async def get_favorites(current_username: str = Depends(get_current_user),
                        favorites_db: _Base = Depends(get_favorites_db)):
    all_fav = favorites_db.fetch({
        'username': current_username
    }).items

    return all_fav


@router.post('/', status_code=status.HTTP_200_OK)
async def favorite(
        request: schemas.track.Track,
        current_username: str = Depends(get_current_user),
        favorites_db: _Base = Depends(get_favorites_db)
):
    exists = favorites_db.fetch({
        'username': current_username,
        'watch_id': request.watch_id
    }).items

    if len(exists) != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Track with ID {request.watch_id} is already in {current_username}'s favorites"
        )

    result = favorites_db.insert({
        "username": current_username,
        **request.dict(exclude={'__pydantic_initialised__'})
    })

    return result
