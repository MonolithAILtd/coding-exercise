import logging
from typing import Optional
from uuid import UUID
from models import Job, JobStatus
from repositories import JobRepository


class JobService:
    def __init__(self):
        self.repository = JobRepository()
    
    def create_job(self, name: Optional[str]) -> Job:
        """Create a new job with CREATED status"""
        try:
            logging.info(f"Creating new job with name: {name}")
            job = Job(name=name or "")
            created_job = self.repository.create(job)
            logging.info(f"Successfully created job {created_job.id} with name: {name}")
            return created_job
        except Exception:
            raise
    
    def run_job(self, job_id: UUID) -> Optional[Job]:
        """Move job to RUNNING status"""
        try:
            logging.info(f"Attempting to run job {job_id}")
            job = self.repository.get_by_id(job_id)
            if not job:
                logging.error(f"Job {job_id} not found")
                return None
            
            job_check = self.repository.get_by_id(job_id)
            if job_check and job_check.status != JobStatus.CREATED:
                logging.error(f"Job {job_id} cannot be run from status {job_check.status}")
                raise ValueError(f"Job {job_id} cannot be run from status {job_check.status}")
            
            logging.info(f"Moving job {job_id} from {job.status} to RUNNING")
            job.update_status(JobStatus.RUNNING)
            updated_job = self.repository.update(job)
            logging.info(f"Successfully started job {job_id}")
            
            return updated_job
        except Exception:
            raise
    
    def get_job(self, job_id: UUID) -> Optional[Job]:
        """Get job by ID"""
        try:
            logging.info(f"Retrieving job {job_id}")
            job = self.repository.get_by_id(job_id)
            if job:
                logging.info(f"Found job {job_id} with status {job.status}")
            else:
                logging.error(f"Job {job_id} not found")
            return job
        except Exception:
            raise
    
    def get_all_jobs(self) -> list[Job]:
        """Get all jobs"""
        try:
            logging.info("Retrieving all jobs")
            jobs = self.repository.get_all()
            logging.info(f"Found {len(jobs)} jobs")
            return jobs
        except Exception:
            raise