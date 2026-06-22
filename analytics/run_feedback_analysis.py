
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models.models import Feedback
from backend.services.feedback_analyzer import analyze_feedback


def run():
    db = SessionLocal()

    try:
        # Get all feedback that hasn't been analyzed yet
        feedbacks = db.query(Feedback).filter(
            Feedback.sentiment == None
        ).all()

        print(f"Found {len(feedbacks)} unanalyzed feedback records.")

        if not feedbacks:
            print("All feedback already analyzed.")
            return

        for fb in feedbacks:
            result = analyze_feedback(fb.feedback_text)

            fb.sentiment       = result["sentiment"]
            fb.sentiment_score = result["sentiment_score"]
            fb.category        = result["category"]

            print(f"ID {fb.id:3} | {result['sentiment']:8} ({result['sentiment_score']:+.2f}) "
                  f"| {result['category']:15} | {fb.feedback_text[:50]}")

        db.commit()
        print(f"\nDone. {len(feedbacks)} records updated.")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    run()