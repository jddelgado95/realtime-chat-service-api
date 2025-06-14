from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app.db.session import get_db

router = APIRouter()

@router.get("/{user_id}", response_model=schemas.user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter(models.user.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user