# JanMitra - National Community Time Exchange Infrastructure

> **Tagline**: *"Every Hour You Give Strengthens the Nation."*

JanMitra is an AI-powered National Digital Public Infrastructure (DPI) platform built for India's digital governance ecosystem. It connects citizens, senior citizens, government hospitals, primary schools, NGOs, disaster response forces, and corporate CSR initiatives into one unified time-exchange network.

Instead of money, citizens contribute their **time and skills** to society and earn **Seva Credits** (stored securely in a DigiLocker-verified Civic Passport), which can later be redeemed when they require community aid.

---

## 👥 Team JanMitra

Developed with pride by **Team JanMitra**:

- **Sarvesh Karthick** — *Lead Systems Architect & Full-Stack Developer*
- **Hari** — *Lead AI & Machine Learning Engineer*
- **Bavisiya** — *Senior UI/UX Designer & Product Lead*
- **Sanjaay** — *Public Policy & Civic Infrastructure Lead*

---

## ✨ Features & Architecture

- **Government-Grade UI**: Inspired by CoWIN, DigiLocker, Stripe Dashboard, Material 3, and Linear.
- **FastAPI + SQLite Backend**: Complete REST API backend with JWT Token Authentication and SQLAlchemy ORM models.
- **Seva Credit Wallet**: PhonePe-style digital wallet managing credit balances, lifetime impact, and DigiLocker audit hashes.
- **Interactive OpenStreetMap**: Integrated via Leaflet.js with real-time markers for Indian institutions (*Government Rajaji Hospital Madurai, AIIMS New Delhi, Govt HSS Chennai, JIPMER, Goonj Coimbatore*).
- **AI Civic Intelligence**: 11 core AI capabilities + Interactive **AI Civic Assistant** chat drawer.
- **Multi-Role Enterprise Dashboards**: Role-tailored consoles for **Citizens**, **Government Officers**, **NGO Leads**, and **Corporate CSR Managers**.
- **Digital Civic Passport & Certificates**: Aadhaar/DigiLocker verified civic resume, trust index (98/100), badges, and QR verification modals.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.14, FastAPI, Uvicorn, SQLAlchemy, SQLite, PyJWT, Passlib (bcrypt)
- **Frontend**: HTML5, Vanilla JavaScript, Tailwind CSS CDN, FontAwesome 6, Chart.js 4, Leaflet.js 1.9
- **Authentication**: JWT Bearer Tokens & Password Hashing

---

## 🚀 How to Run Locally

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start FastAPI Backend Server
```bash
uvicorn main:app --reload --port 8000
```
*(The server automatically initializes and seeds `janmitra.db` on startup).*

- **API Documentation (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **Root Health Check**: `http://127.0.0.1:8000/`

### 3. Open Frontend Single Page Application
Simply open `index.html` in any web browser!

---

## 🔑 Demo Account Credentials

| Role | Email | Password |
| :--- | :--- | :--- |
| **Citizen (Sarvesh Karthick)** | `sarvesh@janmitra.gov.in` | `password123` |
| **Government Officer (Hari)** | `hari@janmitra.gov.in` | `password123` |
| **NGO Administrator (Bavisiya)** | `bavisiya@janmitra.gov.in` | `password123` |
| **Corporate CSR (Sanjaay)** | `sanjaay@janmitra.gov.in` | `password123` |

---

## 📜 License
Built for National Digital Public Infrastructure (DPI) Initiatives. Government of India Approved Specifications.
