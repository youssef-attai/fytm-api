from deta import _Base
from fastapi import Depends, APIRouter

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
        'user': current_username
    }).items

    return all_fav
