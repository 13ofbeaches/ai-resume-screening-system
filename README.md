🚀 AI Resume Screening System

A full-stack AI-powered resume screening platform built using:

FastAPI (Backend API)

Next.js 16 (Frontend UI)

SQLite (Database)

LLM-based Classification

AWS S3 Integration (optional)

Email & WhatsApp Notifications

📌 Project Architecture
ai-resume-screening-system/
│
├── backend/      → FastAPI backend & database logic
├── frontend/     → Next.js frontend application
└── README.md
⚙️ Backend (FastAPI)

Located in:

backend/
Features:

Resume submission endpoint

Candidate classification using LLM

SQLite database storage

Candidate status tracking

REST API endpoints

Run Backend
cd backend
uvicorn api:app --reload

API runs at:

http://127.0.0.1:8000

Available endpoints:

GET /submit

GET /candidates

GET /result/{id}

🎨 Frontend (Next.js)

Located in:

frontend/
Features:

Resume submission form

Real-time API integration

Displays classification result

Run Frontend
cd frontend
npm install
npm run dev

Frontend runs at:

http://localhost:3000
🧠 How It Works

User submits resume via frontend.

Frontend calls FastAPI backend.

Backend stores candidate in SQLite.

LLM classifies candidate.

Status updated to "processed".

Result returned to frontend.

📦 Tech Stack

Python 3.13

FastAPI

SQLite

Next.js 16

Node.js 24 LTS

Ollama (LLM runtime)

🔥 Future Improvements

Switch GET → POST with Pydantic validation

Add Authentication

Deploy backend (Render/Railway)

Deploy frontend (Vercel)

Add admin dashboard

Add async DB layer

Dockerize system

👨‍💻 Author

Sarvesh Karthik