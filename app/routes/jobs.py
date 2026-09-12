from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.security import get_current_user
from app.services.ai import analyze_job_description
from app.database import get_db
from app.models import Job, JobAnalysis
from app.schemas import JobCreate, JobResponse, JobAnalysisResponse


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED
)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = Job(
        title=job_data.title,
        company=job_data.company,
        job_description=job_data.job_description
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.post(
    "/{job_id}/analyze",
    response_model=JobAnalysisResponse
)
def analyze_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    # Check cached analysis first
    cached_analysis = (
        db.query(JobAnalysis)
        .filter(JobAnalysis.job_id == job.id)
        .order_by(JobAnalysis.created_at.desc())
        .first()
    )

    if cached_analysis:
        return {
            "job_id": job.id,
            "analysis": cached_analysis.analysis
        }

    # If no cache exists, call Gemini
    analysis = analyze_job_description(
        title=job.title,
        company=job.company,
        job_description=job.job_description
    )

    # Save AI analysis to database
    job_analysis = JobAnalysis(
        job_id=job.id,
        analysis=analysis
    )

    db.add(job_analysis)
    db.commit()
    db.refresh(job_analysis)

    return {
        "job_id": job.id,
        "analysis": analysis
    }