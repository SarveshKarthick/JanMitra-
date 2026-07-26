from database import init_db, SessionLocal, User, CommunityRequest, WalletTransaction, CommunityChallenge
from auth import hash_password

def seed_database():
    init_db()
    db = SessionLocal()

    # Check if seed already exists
    if db.query(User).first():
        print("Database already seeded.")
        db.close()
        return

    print("Seeding database with Team JanMitra & realistic Indian DPI data...")

    # 1. Team JanMitra Users
    u1 = User(
        name="Sarvesh Karthick",
        email="sarvesh@janmitra.gov.in",
        password_hash=hash_password("password123"),
        phone="9876543210",
        role="citizen",
        district="Chennai",
        trust_score=99,
        seva_credits_balance=150.0,
        digilocker_verified=True
    )
    u2 = User(
        name="Hari",
        email="hari@janmitra.gov.in",
        password_hash=hash_password("password123"),
        phone="9876543211",
        role="government",
        district="Madurai",
        trust_score=98,
        seva_credits_balance=210.0,
        digilocker_verified=True
    )
    u3 = User(
        name="Bavisiya",
        email="bavisiya@janmitra.gov.in",
        password_hash=hash_password("password123"),
        phone="9876543212",
        role="ngo",
        district="Coimbatore",
        trust_score=97,
        seva_credits_balance=180.0,
        digilocker_verified=True
    )
    u4 = User(
        name="Sanjaay",
        email="sanjaay@janmitra.gov.in",
        password_hash=hash_password("password123"),
        phone="9876543213",
        role="csr",
        district="Salem",
        trust_score=96,
        seva_credits_balance=320.0,
        digilocker_verified=True
    )

    db.add_all([u1, u2, u3, u4])
    db.commit()

    # 2. Live Community Requests (Realistic Indian Institutions)
    reqs = [
        CommunityRequest(
            title="Hospital OPD Escort for Senior Citizen",
            description="Escort 74-year-old senior citizen through OPD registration and pharmacy queues at Govt Rajaji Hospital.",
            institution_name="Government Rajaji Hospital",
            category="hospital",
            district="Madurai",
            location_lat=9.9252,
            location_lng=78.1198,
            duration_hours=2.0,
            reward_credits=2.0,
            status="open",
            created_by_user_id=u2.id
        ),
        CommunityRequest(
            title="Remedial Mathematics Mentorship",
            description="Teach basic algebra and arithmetic to Class 6 students at Govt Higher Secondary School.",
            institution_name="Government Higher Secondary School",
            category="school",
            district="Chennai",
            location_lat=13.0827,
            location_lng=80.2707,
            duration_hours=2.5,
            reward_credits=2.5,
            status="open",
            created_by_user_id=u1.id
        ),
        CommunityRequest(
            title="Emergency Blood Donor (O-Negative)",
            description="Urgent blood requirement for critical patient at AIIMS Trauma Center.",
            institution_name="AIIMS New Delhi",
            category="blood",
            district="New Delhi",
            location_lat=28.5672,
            location_lng=77.2100,
            duration_hours=1.5,
            reward_credits=3.0,
            status="open",
            created_by_user_id=u2.id
        ),
        CommunityRequest(
            title="Digital Saarthi Smartphone Training",
            description="Assist elderly residents with UPI payments, DigiLocker onboarding, and e-Sanjeevani healthcare app.",
            institution_name="Goonj Community Center",
            category="senior",
            district="Coimbatore",
            location_lat=11.0168,
            location_lng=76.9558,
            duration_hours=2.0,
            reward_credits=2.0,
            status="open",
            created_by_user_id=u3.id
        ),
        CommunityRequest(
            title="Paediatric Care Companion Support",
            description="Non-medical support for parents in paediatric oncology ward.",
            institution_name="JIPMER Hospital",
            category="hospital",
            district="Puducherry",
            location_lat=11.9560,
            location_lng=79.8130,
            duration_hours=3.0,
            reward_credits=3.0,
            status="open",
            created_by_user_id=u3.id
        )
    ]
    db.add_all(reqs)
    db.commit()

    # 3. Wallet Transactions
    txs = [
        WalletTransaction(
            user_id=u1.id,
            activity_name="Remedial Math Mentorship",
            institution_name="Govt HSS Chennai",
            category="Education",
            credits_amount=2.0,
            transaction_type="earned",
            digilocker_tx_hash="0x7f8a9b2c3d4e5f6a",
            status="verified"
        ),
        WalletTransaction(
            user_id=u1.id,
            activity_name="AIIMS OPD Companion",
            institution_name="AIIMS New Delhi",
            category="Healthcare",
            credits_amount=5.0,
            transaction_type="earned",
            digilocker_tx_hash="0x1a2b3c4d5e6f7a8b",
            status="verified"
        ),
        WalletTransaction(
            user_id=u1.id,
            activity_name="Redeemed: Grocery Delivery Support",
            institution_name="JanMitra Express",
            category="Personal Aid",
            credits_amount=1.0,
            transaction_type="spent",
            digilocker_tx_hash="0x9e8d7c6b5a4f3e2d",
            status="settled"
        )
    ]
    db.add_all(txs)
    db.commit()

    # 4. Community Challenges
    challs = [
        CommunityChallenge(
            title="Mission Green Canopy",
            description="Urban afforestation drive planting 50,000 native trees across Metro cities.",
            category="Environment",
            target_goal=50000,
            current_progress=42000,
            district="Chennai"
        ),
        CommunityChallenge(
            title="Digital Saarthi for Seniors",
            description="Empowering 100,000 elderly citizens with UPI and DigiLocker literacy.",
            category="Digital Inclusion",
            target_goal=100000,
            current_progress=64200,
            district="Coimbatore"
        )
    ]
    db.add_all(challs)
    db.commit()

    db.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
