
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from .db import Base

class ResumeRecord(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255))
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(64))
    job_title = Column(String(255))
    location = Column(String(255))
    summary = Column(Text)
    links = Column(JSON)            # list[str]
    core_skills = Column(JSON)      # list[str]
    soft_skills = Column(JSON)      # list[str]
    education = Column(JSON)        # list[dict]
    experience = Column(JSON)       # list[dict]
    projects = Column(JSON)         # list[dict]
    certifications = Column(JSON)   # list[str]
    resume_rating = Column(Integer)
    improvement_areas = Column(Text)
    upskill_suggestions = Column(Text)
    raw_text = Column(Text)
    meta = Column(JSON)             # any other structured blobs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
