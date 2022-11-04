from deta_shared import deta

users_db = deta.Base(name='users')
favorites_db = deta.Base(name='favorites')


def get_users_db():
    return users_db


def get_favorites_db():
    return favorites_db
