from sqlalchemy import Column, Integer, String

from database import Base


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
