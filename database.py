from deta_shared import deta

users_db = deta.Base(name='users')


def get_users_db():
    return users_db
