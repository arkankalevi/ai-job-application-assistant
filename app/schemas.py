from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobCreate(BaseModel):
    title: str
    company: str
    job_description: str


class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    job_description: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobApplicationCreate(BaseModel):
    job_id: int
    status: str = "applied"
    notes: str | None = None


class JobApplicationResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: str
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JobAnalysisResponse(BaseModel):
    job_id: int
    analysis: str

class CoverLetterResponse(BaseModel):
    application_id: int
    cover_letter: str