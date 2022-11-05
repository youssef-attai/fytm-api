import uuid

from deta import _Base
from fastapi import Depends, APIRouter, HTTPException, status

from database import get_users_db, get_track_cache_db
from oauth2 import get_current_user
from utils import assert_current_user

router = APIRouter(
    prefix="/queue",
    tags=["queue"],
)


@router.get('/')
def get_queues(
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

    return {
        qid: [track_cache_db.fetch({'watch_id': watch_id}).items[0] for watch_id in user['queues'][qid]]
        for qid in user['queues'].keys()
    }


@router.post('/')
def save_queue(
        request: list[str],
        current_username: str = Depends(get_current_user),
        users_db: _Base = Depends(get_users_db),
):
    user = assert_current_user(current_username, users_db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User with username "{current_username} does not exist'
        )

    qid = uuid.uuid4().__str__()
    users_db.update({
        'queues': {
            qid: request
            , **user['queues']
        }
    }, user['key'])

    return {qid: request}
