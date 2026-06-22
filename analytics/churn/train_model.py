"""
Churn Prediction Model
======================
Definition of churn used here:
A user is considered churned if they signed up but have NOT
generated any event in the last 14 days.

Features used:
- session_count: how many sessions the user had
- events_total: total events fired
- used_upload: did they upload a resume?
- used_ats: did they complete ATS analysis?
- used_skill_gap: did they view skill gap?
- used_interview: did they generate interview questions?
- used_premium: did they click premium?
- avg_rating: average feedback rating (if any)
- sentiment_score: average sentiment of their feedback
- days_since_signup: age of the account
- is_premium: are they a paying user?
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import numpy as np
from sqlalchemy import text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
import pickle

from backend.database import engine


def build_features() -> pd.DataFrame:
    query = text("""
        WITH user_events AS (
            SELECT
                u.id                                                        AS user_id,
                u.plan,
                u.created_at,
                COUNT(DISTINCT s.id)                                        AS session_count,
                COUNT(e.id)                                                 AS events_total,
                MAX(e.created_at)                                           AS last_event_at,
                MAX(CASE WHEN e.event_name = 'resume_uploaded'
                    THEN 1 ELSE 0 END)                                      AS used_upload,
                MAX(CASE WHEN e.event_name = 'ats_analysis_completed'
                    THEN 1 ELSE 0 END)                                      AS used_ats,
                MAX(CASE WHEN e.event_name = 'skill_gap_viewed'
                    THEN 1 ELSE 0 END)                                      AS used_skill_gap,
                MAX(CASE WHEN e.event_name = 'interview_questions_generated'
                    THEN 1 ELSE 0 END)                                      AS used_interview,
                MAX(CASE WHEN e.event_name = 'premium_clicked'
                    THEN 1 ELSE 0 END)                                      AS used_premium,
                MAX(CASE WHEN e.event_name = 'return_visit'
                    THEN 1 ELSE 0 END)                                      AS had_return_visit
            FROM users u
            LEFT JOIN sessions s ON u.id = s.user_id
            LEFT JOIN events e ON u.id = e.user_id
            GROUP BY u.id, u.plan, u.created_at
        ),
        user_feedback AS (
            SELECT
                user_id,
                AVG(rating)                                                 AS avg_rating,
                AVG(sentiment_score)                                        AS avg_sentiment
            FROM feedback
            WHERE rating IS NOT NULL
            GROUP BY user_id
        )
        SELECT
            ue.user_id,
            ue.session_count,
            ue.events_total,
            ue.used_upload,
            ue.used_ats,
            ue.used_skill_gap,
            ue.used_interview,
            ue.used_premium,
            ue.had_return_visit,
            COALESCE(uf.avg_rating, 3.0)                                   AS avg_rating,
            COALESCE(uf.avg_sentiment, 0.0)                                AS avg_sentiment,
            EXTRACT(DAY FROM NOW() - ue.created_at)                        AS days_since_signup,
            CASE WHEN ue.plan = 'premium' THEN 1 ELSE 0 END               AS is_premium,
            CASE WHEN ue.last_event_at < NOW() - INTERVAL '14 days'
                 OR ue.last_event_at IS NULL
                 THEN 1 ELSE 0 END                                         AS churned
        FROM user_events ue
        LEFT JOIN user_feedback uf ON ue.user_id = uf.user_id
    """)

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df


def train():
    print("Building features...")
    df = build_features()
    print(f"Dataset: {len(df)} users")
    print(f"Churn rate: {df['churned'].mean():.1%}")

    # Features and target
    feature_cols = [
        'session_count', 'events_total', 'used_upload', 'used_ats',
        'used_skill_gap', 'used_interview', 'used_premium', 'had_return_visit',
        'avg_rating', 'avg_sentiment', 'days_since_signup', 'is_premium'
    ]

    X = df[feature_cols]
    y = df['churned']

    # Check class distribution
    print(f"\nClass distribution:\n{y.value_counts()}")

    # Need at least 20 samples per class to train
    if y.value_counts().min() < 10:
        print("\nWarning: Very few samples in one class.")
        print("Model will train but results may not be reliable.")

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    # Train XGBoost
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42
    )
    model.fit(X_train_scaled, y_train)

    # Evaluate
    y_pred  = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]

    print("\n--- Model Evaluation ---")
    print(classification_report(y_test, y_pred,
          target_names=['Retained', 'Churned']))

    try:
        auc = roc_auc_score(y_test, y_proba)
        print(f"AUC-ROC Score: {auc:.3f}")
    except Exception:
        print("AUC-ROC: Cannot calculate with single class in test set.")

    # Feature importance
    importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\n--- Feature Importance ---")
    print(importance.to_string(index=False))

    # Save model and scaler
    os.makedirs('analytics/churn', exist_ok=True)
    with open('analytics/churn/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('analytics/churn/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    with open('analytics/churn/feature_cols.pkl', 'wb') as f:
        pickle.dump(feature_cols, f)

    print("\nModel saved to analytics/churn/")
    return model, scaler, feature_cols, df


if __name__ == "__main__":
    train()