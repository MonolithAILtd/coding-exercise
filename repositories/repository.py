import boto3
import os
from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError
from models import Job, JobStatus


class JobRepository:
    def __init__(self):
        table_name = os.getenv("JOBS_TABLE_NAME", "jobs")
        self.dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        self.table = self.dynamodb.Table(table_name)
    
    def _job_to_item(self, job: Job) -> dict:
        """Convert Job model to DynamoDB item"""
        return {
            "id": str(job.id),
            "name": job.name,
            "status": job.status.value,
            "statuses": [status.value for status in job.statuses],
            "created_at": job.created_at.isoformat(),
            "updated_at": job.updated_at.isoformat()
        }
    
    def _item_to_job(self, item: dict) -> Job:
        """Convert DynamoDB item to Job model"""
        return Job(
            id=UUID(item["id"]),
            name=item["name"],
            status=JobStatus(item["status"]),
            statuses=[JobStatus(status) for status in item["statuses"]],
            created_at=datetime.fromisoformat(item["created_at"]),
            updated_at=datetime.fromisoformat(item["updated_at"])
        )
    
    def create(self, job: Job) -> Job:
        """Create a new job in DynamoDB"""
        try:
            item = self._job_to_item(job)
            self.table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(id)"
            )
            return job
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise ValueError(f"Job with id {job.id} already exists")
            raise
    
    def get_by_id(self, job_id: UUID) -> Optional[Job]:
        """Get job by ID"""
        try:
            response = self.table.get_item(Key={"id": str(job_id)})
            if "Item" in response:
                return self._item_to_job(response["Item"])
            return None
        except ClientError:
            return None
    
    def update(self, job: Job) -> Job:
        """Update existing job"""
        job.updated_at = datetime.utcnow()
        item = self._job_to_item(job)
        
        try:
            self.table.put_item(Item=item)
            return job
        except ClientError as e:
            raise ValueError(f"Failed to update job {job.id}: {str(e)}")
    
    def delete_by_id(self, job_id: UUID) -> bool:
        """Delete job by ID"""
        try:
            self.table.delete_item(
                Key={"id": str(job_id)},
                ConditionExpression="attribute_exists(id)"
            )
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return False
            raise
    
    def get_all(self) -> list[Job]:
        """Get all jobs"""
        try:
            response = self.table.scan()
            jobs = []
            for item in response.get("Items", []):
                jobs.append(self._item_to_job(item))
            return jobs
        except ClientError:
            return []
    
    def store(self, job: Job) -> Job:
        """Store job (create or update)"""
        item = self._job_to_item(job)
        self.table.put_item(Item=item)
        return job