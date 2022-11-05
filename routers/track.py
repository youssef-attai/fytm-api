from deta import _Base
from fastapi import APIRouter, Depends

from database import get_track_cache_db
from utils import cache_track

router = APIRouter(
    prefix="/track",
    tags=["track"],
)


@router.get('/{watch_id}')
async def track(watch_id: str, track_cache_db: _Base = Depends(get_track_cache_db)):
    cached_track = track_cache_db.fetch({
        "watch_id": watch_id
    }).items

    # If track is not in cached db
    if len(cached_track) == 0:
        # Get track from YouTube
        return cache_track(watch_id, track_cache_db)

    # If track is cached
    return cached_track[0]
