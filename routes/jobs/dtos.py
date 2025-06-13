from pydantic import BaseModel
from typing import Optional


class CreateJobRequest(BaseModel):
    name: Optional[str] = None


class JobResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str