from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models.db_models import User, StudentProfile, RecruiterProfile
from utils.auth import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: str # 'student', 'recruiter', 'admin'
    company_name: Optional[str] = None # For recruiter
    
class UserLogin(BaseModel):
    email: str
    password: str
    role: str

@router.post("/register")
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        password_hash=hashed_password,
        name=user.name,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if user.role == "student":
        profile = StudentProfile(user_id=new_user.id)
        db.add(profile)
    elif user.role == "recruiter":
        profile = RecruiterProfile(user_id=new_user.id, company_name=user.company_name or "Unknown Company")
        db.add(profile)
    
    db.commit()
    
    access_token = create_access_token(data={"sub": new_user.email, "role": new_user.role, "user_id": new_user.id})
    return {"access_token": access_token, "token_type": "bearer", "user": {"id": new_user.id, "email": new_user.email, "role": new_user.role, "name": new_user.name}}

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email, User.role == user.role).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials or role mismatch")
    
    access_token = create_access_token(data={"sub": db_user.email, "role": db_user.role, "user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer", "user": {"id": db_user.id, "email": db_user.email, "role": db_user.role, "name": db_user.name}}
