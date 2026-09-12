from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.security import get_current_user
from app.database import get_db
from app.models import Job, JobApplication
from app.schemas import JobApplicationCreate, JobApplicationResponse


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