from fastapi import APIRouter
from schemas import user as user_schema
from fastapi import Depends
from oauth2 import get_current_user
from repository import track as track_repository

router = APIRouter(
    prefix="/track",
    tags=["tracks"],
)

@router.get('/')
def my_test(current_user: user_schema.User = Depends(get_current_user)):
    return track_repository.my_test()