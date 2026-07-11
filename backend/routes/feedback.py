from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.models import Feedback, Event
from backend.schemas.schemas import FeedbackSubmit, FeedbackResponse
from backend.services.mixpanel_tracker import track

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/submit", response_model=FeedbackResponse)
def submit_feedback(data: FeedbackSubmit, db: Session = Depends(get_db)):
    if data.rating is not None and not (1 <= data.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")

    feedback = Feedback(
        user_id=data.user_id,
        feedback_text=data.feedback_text,
        rating=data.rating
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    if data.user_id:
        event = Event(
            user_id=data.user_id,
            event_name="feedback_submitted",
            event_properties={
                "rating": data.rating,
                "feedback_length": len(data.feedback_text)
            },
            page="/feedback"
        )
        db.add(event)
        db.commit()

        # Track in Mixpanel
        track(str(data.user_id), "feedback_submitted", {
            "rating": data.rating,
            "feedback_length": len(data.feedback_text)
        })

    return FeedbackResponse(id=feedback.id, message="Feedback submitted. Thank you.")


@router.get("/all")
def get_all_feedback(db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).order_by(Feedback.created_at.desc()).all()
    return [
        {
            "id": f.id,
            "user_id": f.user_id,
            "feedback_text": f.feedback_text,
            "rating": f.rating,
            "sentiment": f.sentiment,
            "category": f.category,
            "created_at": str(f.created_at)
        }
        for f in feedbacks
    ]