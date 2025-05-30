from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.db.session import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.auth import Token

router = APIRouter()

@router.post("/signup", response_model=schemas.user.User, status_code=status.HTTP_201_CREATED)
def signup(user_in: schemas.user.UserCreate, db: Session = Depends(get_db)):
    hashed = get_password_hash(user_in.password)
    db_user = models.user.User(email=user_in.email, hashed_password=hashed)
    db.add(db_user)
    db.commit(); db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.user.User).filter_by(email=form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}