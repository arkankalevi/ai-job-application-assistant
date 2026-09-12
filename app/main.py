from fastapi import FastAPI

from app.database import Base, engine
from app.routes.jobs import router as jobs_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Job Application Assistant",
    version="1.0.0"
)


app.include_router(jobs_router)


@app.get("/")
def root():
    return {
        "message": "AI Job Application Assistant API is running"
    }