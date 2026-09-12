from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.security import get_current_user
from app.database import get_db
from app.models import Job
from app.schemas import JobCreate, JobResponse


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