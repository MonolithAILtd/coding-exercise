from enum import Enum
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class JobStatus(str, Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Job(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    status: JobStatus = JobStatus.CREATED
    statuses: List[JobStatus] = Field(default_factory=lambda: [JobStatus.CREATED])
    created_at: datetime = Field(default_factory=datetime.utcnow)  # UTC
    updated_at: datetime = Field(default_factory=datetime.now)     # Local time - inconsistent!
    
    def update_status(self, new_status: JobStatus) -> None:
        self.status = new_status
        if new_status not in self.statuses:
            self.statuses.append(new_status)
        
        if new_status == JobStatus.RUNNING:
            self.updated_at = datetime.now()
        else:
            self.updated_at = datetime.utcnow()