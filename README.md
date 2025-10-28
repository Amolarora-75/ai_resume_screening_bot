
# AI Resume Screening Bot

A full‑stack app that parses resumes (PDF), extracts structured data, rates the resume, and suggests improvements/upskilling with Gemini (via LangChain). 
UI matches the provided screenshots: dark theme, 2 tabs — **Upload** (live) and **History** (past uploads with Details modal).

## Features
- FastAPI backend
- Postgres via SQLAlchemy (with **SQLite fallback** for quick run)
- PDF text extraction (pdfminer.six)
- Basic entity extraction (name, emails, phones, skills, education, experience, projects, links)
- LLM analysis with Gemini (optional: set `GEMINI_API_KEY`) — graceful fallback to rule‑based suggestions
- React + Vite + Tailwind frontend (dark, minimal UI)
- History table + Details modal
- `sample_data/` with example PDFs placeholder
- Docker Compose for one‑command Postgres + backend
- CORS enabled for local dev

## Quick Start

### Option A — Quick Run (SQLite only)
Best for testing without installing Postgres.

```bash
# 1) Backend
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

# (Optional) enable Gemini LLM:
# set GEMINI_API_KEY=<your key>

# Start API (SQLite auto-creates ./app.db)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
# 2) Frontend
cd ../frontend
npm install
npm run dev
```

Open the app at http://localhost:5173 (frontend). It will call the API at http://localhost:8000.

### Option B — Postgres (recommended for assignment)
Using Docker Compose (you only need Docker installed).

```bash
# Start Postgres and pgAdmin (optional) + backend API container
docker compose up --build
```

The backend API will be at http://localhost:8000 and Postgres at localhost:5432 (user: `resume`, pass: `resume`, db: `resume_db`).

### Option C — Manual Postgres (without Docker)
Create a Postgres DB and set environment variables in `backend/.env`:

```
DATABASE_URL=postgresql+psycopg2://<user>:<password>@<host>:5432/<db>
GEMINI_API_KEY=...         # optional
```

Then run the backend as in Option A (but with Postgres packages installed).

## Running End‑to‑End
1. Start the backend (Option A or B).
2. Start the frontend.
3. In the **Upload** tab, paste a job description and upload one or more PDFs.
4. The parsed records appear in the **History** tab. Click **Details** to see the full parsed JSON in a neat layout.

## Prerequisites
- **Frontend**: Node.js 18+ and npm
- **Backend**: Python 3.10+
- **Optional**: Docker Desktop (for Postgres via Docker)
- **Windows users**: If `python` not found, install from python.org and ensure “Add to PATH” is checked.

## Screenshots
Add your screenshots to `screenshots/` (included in repo to meet submission criteria).

## Notes on LLM
- By default, if `GEMINI_API_KEY` is **not** set, the backend returns reasonable rule‑based suggestions to avoid failures.
- If `GEMINI_API_KEY` is set, the app uses LangChain + Gemini for resume review and upskilling hints.

## API
- `POST /api/parse` — multipart form:
  - `job_description` (string, optional)
  - `files` (one or more PDF files)
- `GET /api/resumes` — list of stored rows (summary fields)
- `GET /api/resumes/{id}` — full details for one row

---

Created to match your assignment and provided UI screenshots.
