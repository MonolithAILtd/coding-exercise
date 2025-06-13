# Monolith Exercise

This file provides guidance when working with code in this repository.

## Development Commands

- **Start development server**: `poetry run uvicorn main:app --reload`
- **Install dependencies**: `poetry install`
- **Add new dependency**: `poetry add <package>`
- **Run in production**: `poetry run uvicorn main:app --host 0.0.0.0 --port 8000`

## Project Structure

This is a FastAPI application using Poetry for dependency management:

- `main.py` - Main FastAPI application entry point with route definitions
- `models/` - Pydantic models including Job and JobStatus
- `repositories/` - DynamoDB repository for Job CRUD operations
- `services/` - Business logic layer for job operations
- `pyproject.toml` - Poetry configuration and dependencies
- Python 3.12 is the target runtime

## Architecture

FastAPI application with DynamoDB backend:

- Single application instance in `main.py`
- Async route handlers for API endpoints
- Pydantic models for data validation
- Service layer for business logic (JobService)
- Repository pattern for data persistence with DynamoDB
- FastAPI automatic OpenAPI documentation available at `/docs`

## Job Status Flow

Jobs follow this status progression:

- CREATED → RUNNING → COMPLETED/FAILED

## DynamoDB Setup

The JobRepository expects a DynamoDB table named "jobs" with:

- Primary key: `id` (String)
- Configure AWS credentials via environment variables or AWS CLI
