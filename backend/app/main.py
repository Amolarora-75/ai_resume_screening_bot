
from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from .config import settings
from .db import Base, engine, SessionLocal
from . import models, schemas
from .pdf import extract_text_from_pdf_bytes
from .utils import find_emails, find_phones, find_urls, extract_skills, guess_name, rate_resume
from .llm import llm_review

app = FastAPI(title="AI Resume Screening Bot API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/parse")
async def parse_resume(
    files: List[UploadFile] = File(...),
    job_description: Optional[str] = Form("")
):
    results = []
    db: Session = next(get_db())

    for uf in files:
        data = await uf.read()
        text = extract_text_from_pdf_bytes(data)

        emails = find_emails(text)
        phones = find_phones(text)
        urls = find_urls(text)
        skills = extract_skills(text)
        name = guess_name(text)

        llm = llm_review(text, job_description)

        record = models.ResumeRecord(
            file_name=uf.filename,
            name=name or (emails[0].split("@")[0].replace(".", " ").title() if emails else ""),
            email=emails[0] if emails else None,
            phone=phones[0] if phones else None,
            job_title=None,
            location=None,
            summary=None,
            links=urls,
            core_skills=skills,
            soft_skills=[],
            education=[],
            experience=[],
            projects=[],
            certifications=[],
            resume_rating=llm.get("resume_rating") or rate_resume(skills),
            improvement_areas=llm.get("improvement_areas"),
            upskill_suggestions=llm.get("upskill_suggestions"),
            raw_text=text,
            meta={"job_description_present": bool(job_description)}
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        results.append({
            "id": record.id,
            "file_name": record.file_name,
            "name": record.name,
            "email": record.email,
            "phone": record.phone,
            "links": record.links,
            "core_skills": record.core_skills,
            "soft_skills": record.soft_skills,
            "resume_rating": record.resume_rating,
            "improvement_areas": record.improvement_areas,
            "upskill_suggestions": record.upskill_suggestions,
        })

    return {"ok": True, "count": len(results), "items": results}

@app.get("/api/resumes", response_model=List[schemas.ResumeOut])
def list_resumes(db: Session = Depends(get_db)):
    rows = db.query(models.ResumeRecord).order_by(models.ResumeRecord.id.desc()).all()
    return rows

@app.get("/api/resumes/{rid}", response_model=schemas.ResumeDetail)
def get_resume(rid: int, db: Session = Depends(get_db)):
    row = db.query(models.ResumeRecord).get(rid)
    if not row:
        return {}
    return row
