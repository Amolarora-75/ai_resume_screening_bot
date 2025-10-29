#  AI-Based Resume Screening Bot

###  Overview  
This project implements an **AI-powered Resume Parser and Analyzer** using **FastAPI (Python)** for the backend and **React + Vite** for the frontend.  
It allows users to upload resumes (PDF), automatically extracts structured information, analyzes the resume using a **Gemini LLM (via LangChain)**, and suggests personalized upskilling recommendations.

---

##  Project Structure

```
ai_resume_screening_bot/
│
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI entry point
│ │ ├── models.py # SQLAlchemy models for DB
│ │ ├── database.py # PostgreSQL connection setup
│ │ ├── routes/
│ │ │ ├── resume_routes.py # API routes for upload/fetch
│ │ ├── utils/
│ │ │ ├── parser.py # Resume text extraction logic
│ │ │ ├── ai_analysis.py # LLM (Gemini/LangChain) logic
│ │ └── init.py
│ │
│ ├── requirements.txt # Python dependencies
│ ├── Dockerfile # Backend Docker build file
│ ├── .env # Environment variables (local)
│ └── README.md
│
├── frontend/
│ ├── src/
│ │ ├── components/ # Reusable React components
│ │ ├── pages/
│ │ │ ├── UploadResume.jsx # Upload tab UI
│ │ │ ├── PastResumes.jsx # Past resumes tab UI
│ │ ├── App.jsx # Main React app
│ │ ├── main.jsx # React entry point
│ │ └── api.js # Frontend API integration
│ │
│ ├── vite.config.js # Vite configuration
│ ├── package.json # Node dependencies
│ ├── tailwind.config.js # Tailwind setup
│ ├── index.html
│ └── Dockerfile # Frontend Docker build file
│
├── docker-compose.yml # Docker multi-service config
├── sample_data/ # Test resumes for demo
├── screenshots/ # Project screenshots
└── README.md # Main documentation
```
---

##  Features

###  **Tab 1 – Upload Resume**
- Upload PDF resumes.  
- Backend extracts key fields:  
  - Name, Email, Phone Number  
  - Core & Soft Skills  
  - Experience, Education (if available)  
- Uses **Gemini LLM (via LangChain)** for:
  - Resume improvement suggestions  
  - Personalized upskilling advice  
- Stores parsed data in **PostgreSQL**  
- Displays structured JSON response visually on frontend.

###  **Tab 2 – Past Resumes**
- Fetches and lists all uploaded resumes from DB.  
- Displays: File Name, Name, Email, Phone, Rating.  
- **Details Modal** shows full analysis (skills, suggestions, etc.).

---

##  Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | React (Vite + Tailwind CSS) |
| **Backend API** | FastAPI (Python) |
| **Database** | PostgreSQL |
| **AI/LLM Integration** | Gemini (via LangChain) |
| **Containerization** | Docker + Docker Compose |
| **Environment Config** | dotenv (.env file) |

---

##  Setup Instructions

###  Option A — Local Run (Quick Setup)

####  Prerequisites
- Python ≥ 3.10  
- Node.js ≥ 18  
- PostgreSQL installed & running  
- (Optional) Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

####  Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
# Run FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs to test APIs.

## Frontend Setup
```
cd frontend
npm install
npm run dev
```


Access the frontend at http://localhost:5173

## Option B — Docker Compose (Recommended for Assignment)
* Prerequisites

* Install Docker Desktop and enable virtualization from BIOS.

* Steps
```
cd ai_resume_screening_bot
docker compose up --build
```

* Backend → http://localhost:8000

* Frontend → http://localhost:5173

* Database → localhost:5432 (DB: resume_db)

## Environment Variables

Create a .env file inside /backend with the following:
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/resume_db
GEMINI_API_KEY=your_gemini_api_key_here
```

(Without the Gemini key, fallback AI responses will be used.)

 ## Sample API Response
 ```
{
  "ok": true,
  "count": 1,
  "items": [
    {
      "file_name": "Amol_Arora_Resume.pdf",
      "name": "Amol Arora",
      "email": "amolarora77@gmail.com",
      "phone": "+91 9557681927",
      "core_skills": ["Python","React","Node","Flask","MongoDB","Postgres"],
      "resume_rating": 8,
      "improvement_areas": "Add quantified metrics; highlight major achievements.",
      "upskill_suggestions": "Learn FastAPI deployment, CI/CD basics, and system design."
    }
  ]
}
```
## Key Learning Outcomes

* Building REST APIs with FastAPI

* Using LangChain for LLM integration

* Connecting PostgreSQL with SQLAlchemy ORM

* Multi-container app setup via Docker Compose

* Managing API requests and state in React (Vite)

 ## Assignment Compliance Checklist 

* Frontend UI (Upload + History Tabs)

* Backend with FastAPI & LLM Integration

* PostgreSQL Database Integration

* Resume Parsing & Analysis

* Dockerized Setup for Deployment

* AI Feedback via Gemini (or fallback)

* README as per assignment guidelines

* Screenshots of working app

## Screenshots
<img width="1355" height="638" alt="resumeai 1" src="https://github.com/user-attachments/assets/f2738fbc-cbd0-4d25-9e14-3ae9e563e631" />
<img width="1352" height="722" alt="resumeai 2" src="https://github.com/user-attachments/assets/dcf2e519-cdf4-4c8c-97d1-c8d6070d846d" />
<img width="1357" height="638" alt="resumeai 3" src="https://github.com/user-attachments/assets/6ca286a7-9371-4c83-a7aa-8b9217317460" />
<img width="1363" height="557" alt="resumeai 4" src="https://github.com/user-attachments/assets/f802337d-a199-46af-bbeb-be4f86c08420" />


## Developed By

**Amol Arora**
B.Tech IT (2022–2026), Jaypee University of Information Technology
📧 amolarora77@gmail.com



