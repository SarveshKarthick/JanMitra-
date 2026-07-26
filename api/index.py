from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def _send_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_OPTIONS(self):
        self._send_headers(200)

    def do_GET(self):
        self._send_headers(200)
        path = self.path

        if "/api/requests" in path:
            res = [
                {"id": 1, "title": "Hospital OPD Escort for Senior Citizen", "description": "Escort senior citizen through OPD queues", "institution_name": "Government Rajaji Hospital", "category": "hospital", "district": "Madurai", "location_lat": 9.9252, "location_lng": 78.1198, "duration_hours": 2.0, "reward_credits": 2.0, "status": "open"},
                {"id": 2, "title": "Remedial Mathematics Mentorship", "description": "Teach Class 6 students remedial math", "institution_name": "Government Higher Secondary School", "category": "school", "district": "Chennai", "location_lat": 13.0827, "location_lng": 80.2707, "duration_hours": 2.5, "reward_credits": 2.5, "status": "open"},
                {"id": 3, "title": "Emergency Blood Donor (O-Negative)", "description": "Urgent blood requirement for trauma patient", "institution_name": "AIIMS New Delhi", "category": "blood", "district": "New Delhi", "location_lat": 28.5672, "location_lng": 77.2100, "duration_hours": 1.5, "reward_credits": 3.0, "status": "open"},
                {"id": 4, "title": "Digital Saarthi Smartphone Training", "description": "Assist elderly residents with UPI & DigiLocker", "institution_name": "Goonj Community Center", "category": "senior", "district": "Coimbatore", "location_lat": 11.0168, "location_lng": 76.9558, "duration_hours": 2.0, "reward_credits": 2.0, "status": "open"}
            ]
        elif "/api/wallet/ledger" in path:
            res = {
                "balance": 150.0,
                "transactions": [
                    {"id": 1, "activity_name": "Remedial Math Mentorship", "institution_name": "Govt HSS Chennai", "category": "Education", "credits_amount": 2.0, "transaction_type": "earned", "digilocker_tx_hash": "0x7f8a9b2c3d4e5f6a", "status": "verified", "date": "Today"},
                    {"id": 2, "activity_name": "AIIMS OPD Companion", "institution_name": "AIIMS New Delhi", "category": "Healthcare", "credits_amount": 5.0, "transaction_type": "earned", "digilocker_tx_hash": "0x1a2b3c4d5e6f7a8b", "status": "verified", "date": "Yesterday"},
                    {"id": 3, "activity_name": "Redeemed: Grocery Delivery", "institution_name": "JanMitra Express", "category": "Personal Aid", "credits_amount": 1.0, "transaction_type": "spent", "digilocker_tx_hash": "0x9e8d7c6b5a4f3e2d", "status": "settled", "date": "22 Jul 2026"}
                ]
            }
        elif "/api/team" in path:
            res = {
                "team_name": "Team JanMitra",
                "members": [
                    {"name": "Sarvesh Karthick", "role": "Lead Architect & Full Stack Developer"},
                    {"name": "Hari", "role": "Lead AI Engineer"},
                    {"name": "Bavisiya", "role": "Senior UI/UX Designer"},
                    {"name": "Sanjaay", "role": "Public Policy & Systems Lead"}
                ]
            }
        else:
            res = {
                "status": "online",
                "service": "JanMitra National Digital Public Infrastructure (DPI)",
                "version": "2.4.0",
                "team": ["Sarvesh Karthick", "Hari", "Bavisiya", "Sanjaay"]
            }
        self.wfile.write(json.dumps(res).encode('utf-8'))

    def do_POST(self):
        self._send_headers(200)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(post_data.decode('utf-8'))
        except Exception:
            payload = {}

        path = self.path
        if "/api/auth/login" in path:
            email = payload.get("email", "sarvesh@janmitra.gov.in")
            name = "Sarvesh Karthick"
            if "hari" in email: name = "Hari"
            elif "bavisiya" in email: name = "Bavisiya"
            elif "sanjaay" in email: name = "Sanjaay"

            res = {
                "access_token": "janmitra_vercel_jwt_2026",
                "user": {
                    "id": 1,
                    "name": name,
                    "email": email,
                    "role": "citizen",
                    "district": "Chennai",
                    "trust_score": 99,
                    "seva_credits_balance": 150.0
                }
            }
        elif "/api/wallet/simulate-earn" in path:
            res = {"message": "Earned +2.0 Seva Credits", "new_balance": 152.0}
        elif "/api/ai/assistant" in path:
            prompt = payload.get("prompt", "").lower()
            if "team" in prompt or "creator" in prompt or "who" in prompt:
                resp = "JanMitra was created by Team JanMitra: Sarvesh Karthick (Lead Architect), Hari (AI Lead), Bavisiya (UI/UX Lead), and Sanjaay (Public Policy Lead)."
            elif "credit" in prompt or "wallet" in prompt:
                resp = "Seva Credits are earned by contributing verified hours of service to government hospitals, schools, and NGOs. 1 hour = 1 Seva Credit (valued at ₹350 economic impact)."
            else:
                resp = f"JanMitra AI Engine processed query: '{payload.get('prompt', '')}'. Proximity matching algorithm prioritized urgent requests within Chennai and Madurai districts."
            res = {"response": resp}
        else:
            res = {"message": "Task Accepted & Synced"}
        
        self.wfile.write(json.dumps(res).encode('utf-8'))
