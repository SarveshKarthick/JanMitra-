import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///./janmitra.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(String, default="citizen")  # citizen, government, ngo, csr
    district = Column(String, default="Chennai")
    trust_score = Column(Integer, default=98)
    seva_credits_balance = Column(Float, default=150.0)
    digilocker_verified = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    requests = relationship("CommunityRequest", back_populates="creator")
    wallet_transactions = relationship("WalletTransaction", back_populates="user")

class CommunityRequest(Base):
    __tablename__ = "community_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    institution_name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # hospital, school, blood, senior, disaster, environment
    district = Column(String, default="Chennai")
    location_lat = Column(Float, default=13.0827)
    location_lng = Column(Float, default=80.2707)
    duration_hours = Column(Float, default=2.0)
    reward_credits = Column(Float, default=2.0)
    status = Column(String, default="open")  # open, assigned, completed
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("User", foreign_keys=[created_by_user_id], back_populates="requests")

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_name = Column(String, nullable=False)
    institution_name = Column(String, nullable=False)
    category = Column(String, default="Community Aid")
    credits_amount = Column(Float, nullable=False)
    transaction_type = Column(String, default="earned")  # earned, spent
    digilocker_tx_hash = Column(String, nullable=False)
    status = Column(String, default="verified")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="wallet_transactions")

class CommunityChallenge(Base):
    __tablename__ = "community_challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)
    target_goal = Column(Integer, nullable=False)
    current_progress = Column(Integer, nullable=False)
    district = Column(String, default="Chennai")
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
