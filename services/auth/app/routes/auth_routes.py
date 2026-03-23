from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.db import get_db
from app.models.user_model import User
from app.schemas.user_schema import UserRegister, UserLogin, UserResponse
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_token
from app.utils.dependencies import get_current_user


router = APIRouter()

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    
    try:
        existing_user = db.query(User).filter(
            User.username == user.username
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "Registration successful"}
    except:
        raise HTTPException(
                status_code=400,
                detail="Error registering user"
            )
        
@router.get("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.username == user.username  # compare the current entered username with the username of records in User table
    ).first()
    
    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Username not exists! Please sign up"
        )
        
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Wrong password! Enter correct password"
        )
        
    token = create_token(
        {"sub": str(db_user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email
    }