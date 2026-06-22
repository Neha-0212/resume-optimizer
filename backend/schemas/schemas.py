from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ─── AUTH SCHEMAS ───────────────────────────────────────────

class UserSignup(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    full_name: str
    plan: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    plan: str
    created_at: datetime

    class Config:
        from_attributes = True


# ─── RESUME SCHEMAS ─────────────────────────────────────────

class ResumeUploadResponse(BaseModel):
    message: str
    filename: str
    user_id: int


# ─── FEEDBACK SCHEMAS ───────────────────────────────────────

class FeedbackSubmit(BaseModel):
    user_id: Optional[int] = None
    feedback_text: str
    rating: Optional[int] = None

class FeedbackResponse(BaseModel):
    id: int
    message: str