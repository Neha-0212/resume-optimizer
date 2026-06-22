from mixpanel import Mixpanel
from backend.config import settings

mp = Mixpanel(settings.MIXPANEL_TOKEN) if settings.MIXPANEL_TOKEN else None


def track(user_id: str, event_name: str, properties: dict = None):
    if not mp:
        print(f"[Mixpanel] Token missing — skipping: {event_name}")
        return
    props = properties or {}
    props.update({
        "platform": "web",
        "app_version": "1.0.0",
        "environment": settings.ENVIRONMENT
    })
    try:
        mp.track(str(user_id), event_name, props)
        print(f"[Mixpanel] Tracked: {event_name} for user {user_id}")
    except Exception as e:
        print(f"[Mixpanel] Error: {e}")


def identify_user(user_id: str, email: str, full_name: str, plan: str):
    if not mp:
        return
    try:
        mp.people_set(str(user_id), {
            "$email": email,
            "$name": full_name,
            "plan": plan
        })
    except Exception as e:
        print(f"[Mixpanel] identify error: {e}")