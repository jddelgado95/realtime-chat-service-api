from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models
from app.db.session import get_db

router = APIRouter()

@router.get("/")
def list_channels(db: Session = Depends(get_db)):
    return db.query(models.channel.Channel).all()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_channel(name: str, db: Session = Depends(get_db)):
    if db.query(models.channel.Channel).filter_by(name=name).first():
        raise HTTPException(400, detail="Channel already exists")
    channel = models.channel.Channel(name=name)
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel