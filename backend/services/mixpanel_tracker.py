import os
from mixpanel import Mixpanel
from backend.config import settings

# Initialize — if no token, tracking silently does nothing
mp = Mixpanel(settings.MIXPANEL_TOKEN) if settings.MIXPANEL_TOKEN else None


def track(user_id: str, event_name: str, properties: dict = None):
    """
    Send event to Mixpanel.
    user_id: string identifier for the user
    event_name: what happened
    properties: additional context
    """
    if not mp:
        print(f"[Mixpanel] Token missing — skipping: {event_name}")
        return

    props = properties or {}

    # These properties appear on every event automatically
    props.update({
        "platform": "web",
        "app_version": "1.0.0",
        "environment": settings.ENVIRONMENT
    })

    try:
        mp.track(str(user_id), event_name, props)
        print(f"[Mixpanel] Tracked: {event_name} for user {user_id}")
    except Exception as e:
        # Never crash the app because of tracking failure
        print(f"[Mixpanel] Error tracking {event_name}: {e}")


def identify_user(user_id: str, email: str, full_name: str, plan: str):
    """
    Creates or updates a user profile in Mixpanel.
    This enables user-level analysis — not just event-level.
    """
    if not mp:
        return
    try:
        mp.people_set(str(user_id), {
            "$email": email,
            "$name": full_name,
            "plan": plan,
            "app": "Resume Optimizer"
        })
    except Exception as e:
        print(f"[Mixpanel] Error identifying user: {e}")