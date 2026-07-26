import http.server
import socketserver
import json
import sqlite3
import hashlib
import hmac
import base64
import time
import os
from urllib.parse import urlparse, parse_qs

PORT = 8000
DB_FILE = "janmitra.db"
SECRET_KEY = b"janmitra-national-dpi-secret-key-2026"

def hash_password(password: str) -> str:
    salt = "janmitra_salt_2026"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def create_token(user_id: int, email: str, role: str) -> str:
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip("=")
    payload = base64.urlsafe_b64encode(json.dumps({
        "id": user_id,
        "email": email,
        "role": role,
        "exp": int(time.time()) + 86400 * 7
    }).encode()).decode().rstrip("=")
    
    signature_base = f"{header}.{payload}".encode()
    signature = base64.urlsafe_b64encode(hmac.new(SECRET_KEY, signature_base, hashlib.sha256).digest()).decode().rstrip("=")
    return f"{header}.{payload}.{signature}"

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_and_seed_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        phone TEXT,
        role TEXT DEFAULT 'citizen',
        district TEXT DEFAULT 'Chennai',
        trust_score INTEGER DEFAULT 98,
        seva_credits_balance REAL DEFAULT 150.0,
        digilocker_verified INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS community_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        institution_name TEXT NOT NULL,
        category TEXT NOT NULL,
        district TEXT DEFAULT 'Chennai',
        location_lat REAL DEFAULT 13.0827,
        location_lng REAL DEFAULT 80.2707,
        duration_hours REAL DEFAULT 2.0,
        reward_credits REAL DEFAULT 2.0,
        status TEXT DEFAULT 'open',
        created_by_user_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wallet_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        activity_name TEXT NOT NULL,
        institution_name TEXT NOT NULL,
        category TEXT DEFAULT 'Community Aid',
        credits_amount REAL NOT NULL,
        transaction_type TEXT DEFAULT 'earned',
        digilocker_tx_hash TEXT NOT NULL,
        status TEXT DEFAULT 'verified',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()

    # Seed if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        print("Seeding SQLite database with Team JanMitra & realistic Indian data...")
        users = [
            ("Sarvesh Karthick", "sarvesh@janmitra.gov.in", hash_password("password123"), "9876543210", "citizen", "Chennai", 99, 150.0),
            ("Hari", "hari@janmitra.gov.in", hash_password("password123"), "9876543211", "government", "Madurai", 98, 210.0),
            ("Bavisiya", "bavisiya@janmitra.gov.in", hash_password("password123"), "9876543212", "ngo", "Coimbatore", 97, 180.0),
            ("Sanjaay", "sanjaay@janmitra.gov.in", hash_password("password123"), "9876543213", "csr", "Salem", 96, 320.0)
        ]
        cursor.executemany("""
        INSERT INTO users (name, email, password_hash, phone, role, district, trust_score, seva_credits_balance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, users)

        reqs = [
            ("Hospital OPD Escort for Senior Citizen", "Escort senior citizen through OPD queues", "Government Rajaji Hospital", "hospital", "Madurai", 9.9252, 78.1198, 2.0, 2.0, 1),
            ("Remedial Mathematics Mentorship", "Teach Class 6 students remedial math", "Government Higher Secondary School", "school", "Chennai", 13.0827, 80.2707, 2.5, 2.5, 1),
            ("Emergency Blood Donor (O-Negative)", "Urgent blood requirement for trauma patient", "AIIMS New Delhi", "blood", "New Delhi", 28.5672, 77.2100, 1.5, 3.0, 2),
            ("Digital Saarthi Smartphone Training", "Assist elderly residents with UPI & DigiLocker", "Goonj Community Center", "senior", "Coimbatore", 11.0168, 76.9558, 2.0, 2.0, 3)
        ]
        cursor.executemany("""
        INSERT INTO community_requests (title, description, institution_name, category, district, location_lat, location_lng, duration_hours, reward_credits, created_by_user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, reqs)

        txs = [
            (1, "Remedial Math Mentorship", "Govt HSS Chennai", "Education", 2.0, "earned", "0x7f8a9b2c3d4e5f6a", "verified"),
            (1, "AIIMS OPD Companion", "AIIMS New Delhi", "Healthcare", 5.0, "earned", "0x1a2b3c4d5e6f7a8b", "verified"),
            (1, "Redeemed: Grocery Delivery", "JanMitra Express", "Personal Aid", 1.0, "spent", "0x9e8d7c6b5a4f3e2d", "settled")
        ]
        cursor.executemany("""
        INSERT INTO wallet_transactions (user_id, activity_name, institution_name, category, credits_amount, transaction_type, digilocker_tx_hash, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, txs)

        conn.commit()

    conn.close()

class JanMitraAPIHandler(http.server.BaseHTTPRequestHandler):
    
    def _set_cors_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_cors_headers(200)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        if not path:
            path = '/'

        if path == "/":
            self._set_cors_headers(200)
            res = {
                "status": "online",
                "service": "JanMitra National Digital Public Infrastructure (DPI)",
                "version": "2.4.0",
                "team": ["Sarvesh Karthick", "Hari", "Bavisiya", "Sanjaay"]
            }
            self.wfile.write(json.dumps(res).encode())

        elif path == "/api/requests":
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM community_requests ORDER BY id DESC")
            rows = cursor.fetchall()
            reqs = [dict(r) for r in rows]
            conn.close()

            self._set_cors_headers(200)
            self.wfile.write(json.dumps(reqs).encode())

        elif path == "/api/wallet/ledger":
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = 1")
            user = dict(cursor.fetchone())

            cursor.execute("SELECT * FROM wallet_transactions WHERE user_id = 1 ORDER BY id DESC")
            txs = [dict(t) for t in cursor.fetchall()]
            conn.close()

            self._set_cors_headers(200)
            res = {
                "balance": user["seva_credits_balance"],
                "transactions": txs
            }
            self.wfile.write(json.dumps(res).encode())

        elif path == "/api/team":
            self._set_cors_headers(200)
            res = {
                "team_name": "Team JanMitra",
                "members": [
                    {"name": "Sarvesh Karthick", "role": "Lead Architect & Full Stack Developer"},
                    {"name": "Hari", "role": "Lead AI Engineer"},
                    {"name": "Bavisiya", "role": "Senior UI/UX Designer"},
                    {"name": "Sanjaay", "role": "Public Policy & Systems Lead"}
                ]
            }
            self.wfile.write(json.dumps(res).encode())

        else:
            self._set_cors_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(post_data.decode('utf-8'))
        except Exception:
            payload = {}

        if path == "/api/auth/login":
            email = payload.get("email", "")
            password = payload.get("password", "")
            hashed = hash_password(password)

            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ? AND password_hash = ?", (email, hashed))
            row = cursor.fetchone()
            conn.close()

            if row:
                user = dict(row)
                token = create_token(user["id"], user["email"], user["role"])
                self._set_cors_headers(200)
                res = {
                    "access_token": token,
                    "user": {
                        "id": user["id"],
                        "name": user["name"],
                        "email": user["email"],
                        "role": user["role"],
                        "district": user["district"],
                        "trust_score": user["trust_score"],
                        "seva_credits_balance": user["seva_credits_balance"]
                    }
                }
                self.wfile.write(json.dumps(res).encode())
            else:
                self._set_cors_headers(401)
                self.wfile.write(json.dumps({"detail": "Invalid credentials"}).encode())

        elif path == "/api/requests":
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO community_requests (title, description, institution_name, category, district, duration_hours, reward_credits, created_by_user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            """, (
                payload.get("title", "Community Task"),
                payload.get("description", ""),
                payload.get("institution_name", "Government Institution"),
                payload.get("category", "hospital"),
                payload.get("district", "Chennai"),
                payload.get("duration_hours", 2.0),
                payload.get("reward_credits", 2.0)
            ))
            conn.commit()
            new_id = cursor.lastrowid
            conn.close()

            self._set_cors_headers(200)
            self.wfile.write(json.dumps({"message": "Task Broadcasted Successfully", "id": new_id}).encode())

        elif path == "/api/wallet/simulate-earn":
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET seva_credits_balance = seva_credits_balance + 2.0 WHERE id = 1")
            cursor.execute("""
            INSERT INTO wallet_transactions (user_id, activity_name, institution_name, category, credits_amount, transaction_type, digilocker_tx_hash, status)
            VALUES (1, 'Simulated Community Task', 'Government DPI Portal', 'Community Aid', 2.0, 'earned', ?, 'verified')
            """, (f"0x{int(time.time())}",))
            conn.commit()
            
            cursor.execute("SELECT seva_credits_balance FROM users WHERE id = 1")
            new_bal = cursor.fetchone()[0]
            conn.close()

            self._set_cors_headers(200)
            self.wfile.write(json.dumps({"message": "Earned +2.0 Seva Credits", "new_balance": new_bal}).encode())

        elif path == "/api/ai/assistant":
            prompt = payload.get("prompt", "").lower()
            if "team" in prompt or "creator" in prompt or "who" in prompt:
                resp = "JanMitra was created by Team JanMitra: Sarvesh Karthick (Lead Architect), Hari (AI Lead), Bavisiya (UI/UX Lead), and Sanjaay (Public Policy Lead)."
            elif "credit" in prompt or "wallet" in prompt:
                resp = "Seva Credits are earned by contributing verified hours of service to government hospitals, schools, and NGOs. 1 hour = 1 Seva Credit (valued at ₹350 economic impact)."
            else:
                resp = f"JanMitra AI Civic Engine processed query: '{payload.get('prompt', '')}'. Proximity matching algorithm prioritized urgent requests within Chennai and Madurai districts."
            
            self._set_cors_headers(200)
            self.wfile.write(json.dumps({"response": resp}).encode())

        else:
            self._set_cors_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

def run_server():
    init_and_seed_db()
    with socketserver.TCPServer(("", PORT), JanMitraAPIHandler) as httpd:
        print(f"JanMitra National DPI Backend Server running on http://127.0.0.1:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
