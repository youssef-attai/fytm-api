from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class ShowUser(BaseModel):
    key: str
    username: str
