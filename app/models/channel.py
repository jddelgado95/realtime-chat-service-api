from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)