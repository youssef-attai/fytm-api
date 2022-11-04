from fastapi import APIRouter

from utils import create_track_from_watch_id

router = APIRouter(
    prefix="/track",
    tags=["track"],
)


@router.get('/{watch_id}')
async def track(watch_id: str):
    return create_track_from_watch_id(watch_id)
