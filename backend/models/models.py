from sqlalchemy import (
    Column, Integer, String, Text, Float,
    Boolean, DateTime, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    plan = Column(String(50), default="free")          # free | premium
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    sessions = relationship("Session", back_populates="user")
    events = relationship("Event", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")
    subscription = relationship("Subscription", back_populates="user", uselist=False)


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_start = Column(DateTime(timezone=True), server_default=func.now())
    session_end = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    device = Column(String(100), nullable=True)        # desktop | mobile | tablet
    source = Column(String(100), nullable=True)        # direct | google | linkedin

    user = relationship("User", back_populates="sessions")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    event_name = Column(String(255), nullable=False, index=True)
    event_properties = Column(JSON, nullable=True)     # flexible key-value store
    page = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="events")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    feedback_text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)            # 1 to 5
    sentiment = Column(String(50), nullable=True)      # positive | neutral | negative
    sentiment_score = Column(Float, nullable=True)     # -1.0 to 1.0
    category = Column(String(100), nullable=True)      # bug | feature_request | praise | complaint
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="feedbacks")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    plan = Column(String(50), default="free")          # free | premium
    status = Column(String(50), default="active")      # active | cancelled | expired
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    amount_paid = Column(Float, default=0.0)

    user = relationship("User", back_populates="subscription")