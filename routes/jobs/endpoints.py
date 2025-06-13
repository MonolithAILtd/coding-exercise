from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID
from models import Job
from services import JobService
from .dtos import CreateJobRequest

router = APIRouter(prefix="/jobs", tags=["jobs"])

def get_job_service() -> JobService:
    return JobService()


@router.post("/new", response_model=Job)
def create_job(
    request: CreateJobRequest,
    job_service: JobService = Depends(get_job_service)
):
    try:
        job = job_service.create_job(request.name)
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {repr(e)}, Stack: {e.__traceback__}")


@router.post("/{job_id}/run", response_model=Job)
def run_job(
    job_id: UUID,
    job_service: JobService = Depends(get_job_service)
):
    try:
        job = job_service.run_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error in run_job: {type(e).__name__}: {str(e)}")


@router.get("/", response_model=list[Job])
def get_all_jobs(
    job_service: JobService = Depends(get_job_service)
):
    try:
        jobs = job_service.get_all_jobs()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AWS DynamoDB Exception: {e}, Details: {e.__dict__}")


@router.get("/{job_id}", response_model=Job)
def get_job(
    job_id: UUID,
    job_service: JobService = Depends(get_job_service)
):
    try:
        job = job_service.get_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AWS DynamoDB Exception: {e}, Details: {e.__dict__}")