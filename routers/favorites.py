from deta import _Base
from fastapi import Depends, APIRouter, HTTPException, status

import schemas.track
from database import get_users_db, get_track_cache_db
from oauth2 import get_current_user
from utils import cache_track, assert_current_user

router = APIRouter(
    prefix="/favorite",
    tags=["favorite"],
)


@router.get('/')
async def get_favorites(
        current_username: str = Depends(get_current_user),
        users_db: _Base = Depends(get_users_db),
        track_cache_db: _Base = Depends(get_track_cache_db)
):
    user = assert_current_user(current_username, users_db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User with username "{current_username} does not exist'
        )

    return [track_cache_db.fetch({'watch_id': fav}).items[0] for fav in user['favs']]


@router.post('/', status_code=status.HTTP_200_OK)
async def favorite(
        request: schemas.track.TrackWatchID,
        current_username: str = Depends(get_current_user),
        users_db: _Base = Depends(get_users_db),
        track_cache_db: _Base = Depends(get_track_cache_db)
):
    user = assert_current_user(current_username, users_db)

    not_cached = len(track_cache_db.fetch({
        'watch_id': request.watch_id
    }).items) == 0

    if not_cached:
        cache_track(request.watch_id, track_cache_db)

    users_db.update({
        'favs': list({request.watch_id, *user['favs']})
    }, user['key'])

    return {'message': 'Added to your favorites'}
