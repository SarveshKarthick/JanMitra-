from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import get_db, init_db, User, CommunityRequest, WalletTransaction, CommunityChallenge
from auth import hash_password, verify_password, create_access_token, decode_access_token
from seed import seed_database

app = FastAPI(
    title="JanMitra National DPI API",
    description="Backend services for India's AI-Powered Community Time Exchange Platform",
    version="2.4.0"
)

# Enable CORS for frontend Single Page Application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    seed_database()

# Pydantic Schemas
class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str] = None
    role: Optional[str] = "citizen"
    district: Optional[str] = "Chennai"

class UserLogin(BaseModel):
    email: str
    password: str

class RequestCreate(BaseModel):
    title: str
    description: str
    institution_name: str
    category: str
    district: str
    duration_hours: float = 2.0
    reward_credits: float = 2.0

class AIChatQuery(BaseModel):
    prompt: str

# API Routes
@app.get("/")
def root():
    return {
        "status": "online",
        "service": "JanMitra National Digital Public Infrastructure (DPI)",
        "version": "2.4.0",
        "team": ["Sarvesh Karthick", "Hari", "Bavisiya", "Sanjaay"]
    }

@app.post("/api/auth/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        phone=user_data.phone,
        role=user_data.role,
        district=user_data.district,
        trust_score=98,
        seva_credits_balance=150.0,
        digilocker_verified=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email, "id": new_user.id, "role": new_user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role,
            "district": new_user.district,
            "trust_score": new_user.trust_score,
            "seva_credits_balance": new_user.seva_credits_balance
        }
    }

@app.post("/api/auth/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user.email, "id": user.id, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "district": user.district,
            "trust_score": user.trust_score,
            "seva_credits_balance": user.seva_credits_balance
        }
    }

@app.get("/api/requests")
def get_requests(category: Optional[str] = None, district: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(CommunityRequest)
    if category and category != "all":
        query = query.filter(CommunityRequest.category == category)
    if district:
        query = query.filter(CommunityRequest.district == district)
    
    requests = query.order_by(CommunityRequest.created_at.desc()).all()
    return [{
        "id": r.id,
        "title": r.title,
        "description": r.description,
        "institution_name": r.institution_name,
        "category": r.category,
        "district": r.district,
        "location_lat": r.location_lat,
        "location_lng": r.location_lng,
        "duration_hours": r.duration_hours,
        "reward_credits": r.reward_credits,
        "status": r.status
    } for r in requests]

@app.post("/api/requests")
def create_request(req_data: RequestCreate, db: Session = Depends(get_db)):
    # Default to first user if not authenticated
    user = db.query(User).first()
    new_req = CommunityRequest(
        title=req_data.title,
        description=req_data.description,
        institution_name=req_data.institution_name,
        category=req_data.category,
        district=req_data.district,
        duration_hours=req_data.duration_hours,
        reward_credits=req_data.reward_credits,
        status="open",
        created_by_user_id=user.id if user else 1
    )
    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return {"message": "Community request created successfully", "request_id": new_req.id}

@app.post("/api/requests/{request_id}/accept")
def accept_request(request_id: int, db: Session = Depends(get_db)):
    req = db.query(CommunityRequest).filter(CommunityRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    
    req.status = "assigned"
    db.commit()
    return {"message": f"Successfully accepted task: {req.title}"}

@app.get("/api/wallet/ledger")
def get_wallet_ledger(db: Session = Depends(get_db)):
    user = db.query(User).first()
    txs = db.query(WalletTransaction).filter(WalletTransaction.user_id == user.id).order_by(WalletTransaction.created_at.desc()).all()
    return {
        "balance": user.seva_credits_balance,
        "transactions": [{
            "id": t.id,
            "activity_name": t.activity_name,
            "institution_name": t.institution_name,
            "category": t.category,
            "credits_amount": t.credits_amount,
            "transaction_type": t.transaction_type,
            "digilocker_tx_hash": t.digilocker_tx_hash,
            "status": t.status,
            "date": t.created_at.strftime("%Y-%m-%d %H:%M")
        } for t in txs]
    }

@app.post("/api/wallet/simulate-earn")
def simulate_earn(db: Session = Depends(get_db)):
    user = db.query(User).first()
    user.seva_credits_balance += 2.0
    
    new_tx = WalletTransaction(
        user_id=user.id,
        activity_name="Simulated Community Task",
        institution_name="Government DPI Portal",
        category="Community Aid",
        credits_amount=2.0,
        transaction_type="earned",
        digilocker_tx_hash=f"0x{datetime.utcnow().timestamp():.0f}",
        status="verified"
    )
    db.add(new_tx)
    db.commit()
    return {
        "message": "Earned +2.0 Seva Credits",
        "new_balance": user.seva_credits_balance
    }

@app.post("/api/ai/assistant")
def ai_assistant(query: AIChatQuery):
    prompt = query.prompt.lower()
    if "credit" in prompt or "wallet" in prompt:
        resp = "Seva Credits are earned by offering verified hours of service to schools, hospitals, senior citizens, and NGOs. Every 1 hour of service = 1 Seva Credit (valued at ₹350 economic impact)."
    elif "hospital" in prompt or "opd" in prompt:
        resp = "Current hospital requests are active at Government Rajaji Hospital Madurai, AIIMS New Delhi, and JIPMER Puducherry. Escorting senior citizens earns between 2.0 to 3.0 Seva Credits."
    elif "team" in prompt or "creator" in prompt:
        resp = "JanMitra was built by Team JanMitra: Sarvesh Karthick (Lead Architect), Hari (AI Lead), Bavisiya (UI/UX Lead), and Sanjaay (Public Policy Lead)."
    else:
        resp = f"JanMitra AI Civic Engine processed: '{query.prompt}'. Our intelligent matching algorithm prioritizes urgent medical SOS requests and matches skilled volunteers within a 5km radius."
    
    return {"response": resp}

@app.get("/api/team")
def get_team():
    return {
        "team_name": "Team JanMitra",
        "members": [
            {"name": "Sarvesh Karthick", "role": "Lead Architect & Full Stack Engineer"},
            {"name": "Hari", "role": "Lead AI Engineer"},
            {"name": "Bavisiya", "role": "Senior UI/UX Designer"},
            {"name": "Sanjaay", "role": "Public Policy & Systems Lead"}
        ]
    }
