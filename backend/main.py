from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.routes import auth, resume, feedback

app = FastAPI(
    title="Resume Optimizer API",
    description="AI Resume Optimizer and Product Intelligence Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(feedback.router)


@app.get("/")
def root():
    return {
        "status": "running",
        "app": "Resume Optimizer API",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}