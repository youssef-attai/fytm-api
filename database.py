from deta_shared import deta

users_db = deta.Base(name='users')
track_cache_db = deta.Base(name='track_cache')


def get_users_db():
    return users_db


def get_track_cache_db():
    return track_cache_db
