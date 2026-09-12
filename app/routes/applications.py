from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.security import get_current_user
from app.database import get_db
from app.models import Job, JobApplication, CoverLetter
from app.schemas import (
    JobApplicationCreate,
    JobApplicationResponse,
    CoverLetterResponse
)
from app.services.ai import generate_cover_letter


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post(
    "",
    response_model=JobApplicationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_application(
    application_data: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = (
        db.query(Job)
        .filter(Job.id == application_data.job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    application = JobApplication(
        user_id=current_user.id,
        job_id=application_data.job_id,
        status=application_data.status,
        notes=application_data.notes
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@router.get(
    "",
    response_model=list[JobApplicationResponse]
)
def get_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    applications = (
        db.query(JobApplication)
        .filter(JobApplication.user_id == current_user.id)
        .all()
    )

    return applications


@router.post(
    "/{application_id}/cover-letter",
    response_model=CoverLetterResponse
)
def create_cover_letter(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = (
        db.query(JobApplication)
        .filter(
            JobApplication.id == application_id,
            JobApplication.user_id == current_user.id
        )
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    job = (
        db.query(Job)
        .filter(Job.id == application.job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    # Check if a cover letter already exists
    existing_cover_letter = (
        db.query(CoverLetter)
        .filter(
            CoverLetter.application_id == application.id
        )
        .order_by(CoverLetter.created_at.desc())
        .first()
    )

    if existing_cover_letter:
        return {
            "application_id": application.id,
            "cover_letter": existing_cover_letter.content
        }

    # Generate a new cover letter with Gemini
    cover_letter = generate_cover_letter(
        title=job.title,
        company=job.company,
        job_description=job.job_description
    )

    # Save cover letter to database
    new_cover_letter = CoverLetter(
        application_id=application.id,
        content=cover_letter
    )

    db.add(new_cover_letter)
    db.commit()
    db.refresh(new_cover_letter)

    return {
        "application_id": application.id,
        "cover_letter": new_cover_letter.content
    }