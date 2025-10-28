
from pydantic import BaseModel, Field
from typing import List, Optional, Any

class ResumeOut(BaseModel):
    id: int
    file_name: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    core_skills: List[str] = []
    soft_skills: List[str] = []
    resume_rating: Optional[int] = None

    class Config:
        from_attributes = True

class ResumeDetail(BaseModel):
    id: int
    file_name: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    links: List[str] = []
    core_skills: List[str] = []
    soft_skills: List[str] = []
    education: Any = None
    experience: Any = None
    projects: Any = None
    certifications: Any = None
    resume_rating: Optional[int] = None
    improvement_areas: Optional[str] = None
    upskill_suggestions: Optional[str] = None
    raw_text: Optional[str] = None
    meta: Any = None

    class Config:
        from_attributes = True
