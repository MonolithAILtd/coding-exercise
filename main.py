from fastapi import FastAPI
from routes import jobs_router

app = FastAPI()

app.include_router(jobs_router)