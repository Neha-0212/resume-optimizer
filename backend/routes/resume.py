from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import os

from backend.database import get_db
from backend.models.models import Event
from backend.schemas.schemas import ResumeUploadResponse
from backend.services.resume_analyzer import analyze_resume
from backend.services.mixpanel_tracker import track

router = APIRouter(prefix="/resume", tags=["Resume"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain"
]
MAX_FILE_SIZE_MB = 5


@router.post("/upload", response_model=ResumeUploadResponse)
def upload_resume(
    user_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are allowed.")

    contents = file.file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"File too large. Max {MAX_FILE_SIZE_MB}MB.")

    safe_filename = f"user_{user_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    # Log to database
    event = Event(
        user_id=user_id,
        event_name="resume_uploaded",
        event_properties={
            "file_type": file.content_type,
            "file_size_kb": round(len(contents) / 1024, 2),
            "filename": file.filename
        },
        page="/upload"
    )
    db.add(event)
    db.commit()

    # Track in Mixpanel
    track(str(user_id), "resume_uploaded", {
        "file_type": file.content_type,
        "file_size_kb": round(len(contents) / 1024, 2)
    })

    return ResumeUploadResponse(
        message="Resume uploaded successfully.",
        filename=safe_filename,
        user_id=user_id
    )

@router.post("/analyze")
def analyze_resume_endpoint(
    user_id: int = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCX, and TXT files are allowed."
        )

    contents = file.file.read()

    if len(contents) / (1024 * 1024) > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail="File too large."
        )

    # -----------------------------
    # Resume Uploaded Event
    # -----------------------------
    resume_upload_event = Event(
        user_id=user_id,
        event_name="resume_uploaded",
        event_properties={
            "file_type": file.content_type,
            "file_size_kb": round(len(contents) / 1024, 2),
            "filename": file.filename
        },
        page="/analyze"
    )

    db.add(resume_upload_event)

    track(str(user_id), "resume_uploaded", {
        "file_type": file.content_type,
        "file_size_kb": round(len(contents) / 1024, 2),
        "filename": file.filename,
        "source": "analyze_endpoint"
    })

    # -----------------------------
    # Analyze Resume
    # -----------------------------
    result = analyze_resume(
        file_bytes=contents,
        content_type=file.content_type,
        job_description=job_description,
        job_title=job_title
    )

    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    # -----------------------------
    # ATS Analysis Event
    # -----------------------------
    ats_event = Event(
        user_id=user_id,
        event_name="ats_analysis_completed",
        event_properties={
            "ats_score": result["ats_score"],
            "job_title": job_title,
            "missing_skills_count": len(
                result["skill_gap"]["missing_skills"]
            )
        },
        page="/results"
    )

    db.add(ats_event)
    db.commit()

    track(str(user_id), "ats_analysis_completed", {
        "ats_score": result["ats_score"],
        "job_title": job_title,
        "missing_skills_count": len(
            result["skill_gap"]["missing_skills"]
        )
    })

    # -----------------------------
    # Skill Gap Viewed Event
    # -----------------------------
    track(str(user_id), "skill_gap_viewed", {
        "missing_skills": result["skill_gap"]["missing_skills"],
        "match_percentage": result["skill_gap"]["match_percentage"]
    })

    # -----------------------------
    # Interview Questions Generated
    # -----------------------------
    track(str(user_id), "interview_questions_generated", {
        "question_count": len(result["interview_questions"]),
        "job_title": job_title
    })

    return result
