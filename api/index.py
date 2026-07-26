import json

def app(environ, start_response):
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', 'GET')

    status = '200 OK'
    headers = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE'),
        ('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    ]
    start_response(status, headers)

    if method == 'OPTIONS':
        return [b'']

    if '/api/requests' in path:
        data = [
            {"id": 1, "title": "Hospital OPD Escort for Senior Citizen", "description": "Escort senior citizen through OPD queues", "institution_name": "Government Rajaji Hospital", "category": "hospital", "district": "Madurai", "location_lat": 9.9252, "location_lng": 78.1198, "duration_hours": 2.0, "reward_credits": 2.0, "status": "open"},
            {"id": 2, "title": "Remedial Mathematics Mentorship", "description": "Teach Class 6 students remedial math", "institution_name": "Government Higher Secondary School", "category": "school", "district": "Chennai", "location_lat": 13.0827, "location_lng": 80.2707, "duration_hours": 2.5, "reward_credits": 2.5, "status": "open"},
            {"id": 3, "title": "Emergency Blood Donor (O-Negative)", "description": "Urgent blood requirement for trauma patient", "institution_name": "AIIMS New Delhi", "category": "blood", "district": "New Delhi", "location_lat": 28.5672, "location_lng": 77.2100, "duration_hours": 1.5, "reward_credits": 3.0, "status": "open"},
            {"id": 4, "title": "Digital Saarthi Smartphone Training", "description": "Assist elderly residents with UPI & DigiLocker", "institution_name": "Goonj Community Center", "category": "senior", "district": "Coimbatore", "location_lat": 11.0168, "location_lng": 76.9558, "duration_hours": 2.0, "reward_credits": 2.0, "status": "open"}
        ]
    elif '/api/wallet/ledger' in path:
        data = {
            "balance": 150.0,
            "transactions": [
                {"id": 1, "activity_name": "Remedial Math Mentorship", "institution_name": "Govt HSS Chennai", "category": "Education", "credits_amount": 2.0, "transaction_type": "earned", "digilocker_tx_hash": "0x7f8a9b2c3d4e5f6a", "status": "verified", "date": "Today"},
                {"id": 2, "activity_name": "AIIMS OPD Companion", "institution_name": "AIIMS New Delhi", "category": "Healthcare", "credits_amount": 5.0, "transaction_type": "earned", "digilocker_tx_hash": "0x1a2b3c4d5e6f7a8b", "status": "verified", "date": "Yesterday"},
                {"id": 3, "activity_name": "Redeemed: Grocery Delivery", "institution_name": "JanMitra Express", "category": "Personal Aid", "credits_amount": 1.0, "transaction_type": "spent", "digilocker_tx_hash": "0x9e8d7c6b5a4f3e2d", "status": "settled", "date": "22 Jul 2026"}
            ]
        }
    elif '/api/team' in path:
        data = {
            "team_name": "Team JanMitra",
            "members": [
                {"name": "Sarvesh Karthick", "role": "Lead Architect & Full Stack Developer"},
                {"name": "Hari", "role": "Lead AI Engineer"},
                {"name": "Bavisiya", "role": "Senior UI/UX Designer"},
                {"name": "Sanjaay", "role": "Public Policy & Systems Lead"}
            ]
        }
    elif '/api/auth/login' in path:
        data = {
            "access_token": "janmitra_vercel_jwt_2026",
            "user": {
                "id": 1,
                "name": "Sarvesh Karthick",
                "email": "sarvesh@janmitra.gov.in",
                "role": "citizen",
                "district": "Chennai",
                "trust_score": 99,
                "seva_credits_balance": 150.0
            }
        }
    elif '/api/wallet/simulate-earn' in path:
        data = {"message": "Earned +2.0 Seva Credits", "new_balance": 152.0}
    elif '/api/ai/assistant' in path:
        data = {"response": "JanMitra was created by Team JanMitra: Sarvesh Karthick (Lead Architect), Hari (AI Lead), Bavisiya (UI/UX Lead), and Sanjaay (Public Policy Lead)."}
    else:
        data = {
            "status": "online",
            "service": "JanMitra National Digital Public Infrastructure (DPI)",
            "version": "2.4.0",
            "team": ["Sarvesh Karthick", "Hari", "Bavisiya", "Sanjaay"]
        }

    return [json.dumps(data).encode('utf-8')]
