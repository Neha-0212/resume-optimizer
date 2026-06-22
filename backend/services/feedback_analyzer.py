from textblob import TextBlob
import re

# ─── CATEGORY KEYWORDS ───────────────────────────────────────
# Maps complaint/praise categories to keywords
# Expandable — add more as you get real user feedback

CATEGORIES = {
    "performance": [
        "slow", "fast", "speed", "loading", "lag", "takes too long",
        "quick", "instant", "delay", "timeout"
    ],
    "accuracy": [
        "accurate", "inaccurate", "wrong", "correct", "matching",
        "score", "algorithm", "misleading", "off", "precise"
    ],
    "ui_ux": [
        "interface", "ui", "confusing", "easy", "difficult", "design",
        "layout", "navigate", "clean", "cluttered", "intuitive"
    ],
    "features": [
        "feature", "questions", "interview", "skill", "gap", "suggestion",
        "variety", "categories", "role", "specific", "more"
    ],
    "value": [
        "helpful", "useful", "worth", "premium", "price", "value",
        "recommend", "excellent", "great", "good"
    ],
    "onboarding": [
        "signup", "onboard", "start", "figure out", "confusing",
        "what to do", "next step", "tutorial", "guide"
    ]
}


def classify_sentiment(text: str) -> dict:
    """
    Uses TextBlob polarity scoring.
    Polarity: -1.0 (very negative) to +1.0 (very positive)
    Subjectivity: 0.0 (objective) to 1.0 (subjective)
    """
    blob = TextBlob(text)
    polarity = round(blob.sentiment.polarity, 3)
    subjectivity = round(blob.sentiment.subjectivity, 3)

    if polarity >= 0.2:
        label = "positive"
    elif polarity <= -0.2:
        label = "negative"
    else:
        label = "neutral"

    return {
        "sentiment": label,
        "sentiment_score": polarity,
        "subjectivity": subjectivity
    }


def classify_category(text: str) -> str:
    """
    Assigns feedback to the most relevant category
    based on keyword matching.
    Returns 'general' if no category matches.
    """
    text_lower = text.lower()
    scores = {}

    for category, keywords in CATEGORIES.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[category] = score

    if not scores:
        return "general"

    return max(scores, key=scores.get)


def analyze_feedback(text: str) -> dict:
    """
    Master function — runs both sentiment and category analysis.
    """
    sentiment_result = classify_sentiment(text)
    category = classify_category(text)

    return {
        "sentiment": sentiment_result["sentiment"],
        "sentiment_score": sentiment_result["sentiment_score"],
        "subjectivity": sentiment_result["subjectivity"],
        "category": category
    }