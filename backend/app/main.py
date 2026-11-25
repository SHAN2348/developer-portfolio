
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.api.routes import (
    health,
    projects,
    auth,
    portfolio_sections,
    skills,
    education,
    experience,
    certifications,
    achievements,
    resumes,
    contact,
    contact_messages,
    visits
)
from app.db.database import (
    connect_to_mongodb,
    close_mongodb_connection
)

import os
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()

    yield

    await close_mongodb_connection()


app = FastAPI(
    title="Developer Portfolio API",
    description="Backend API for my developer portfolio",
    version="1.0.0",
    lifespan=lifespan
)


# CORS configuration
frontend_origins = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173"
)

allowed_origins = [
    origin.strip()
    for origin in frontend_origins.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/")
async def home():
    return {
        "message": "Welcome to my Developer Portfolio API!",
        "status": "running"
    }


app.include_router(health.router)
app.include_router(projects.router)
app.include_router(auth.router)
app.include_router(portfolio_sections.router)
app.include_router(skills.router)
app.include_router(education.router)
app.include_router(experience.router)
app.include_router(certifications.router)
app.include_router(achievements.router)
app.include_router(resumes.router)
app.include_router(contact.router)
app.include_router(contact_messages.router)
app.include_router(visits.router)