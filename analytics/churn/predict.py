"""
Generates churn risk scores for all users.
Saves results to analytics/churn/churn_scores.csv
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import pickle
from sqlalchemy import text
from backend.database import engine


def predict_churn():
    # Load model artifacts
    with open('analytics/churn/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('analytics/churn/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('analytics/churn/feature_cols.pkl', 'rb') as f:
        feature_cols = pickle.load(f)

    # Load user features
    query = text("""
        WITH user_events AS (
            SELECT
                u.id                                                        AS user_id,
                u.email,
                u.full_name,
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
            GROUP BY u.id, u.email, u.full_name, u.plan, u.created_at
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
            ue.email,
            ue.full_name,
            ue.plan,
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
            ue.last_event_at
        FROM user_events ue
        LEFT JOIN user_feedback uf ON ue.user_id = uf.user_id
    """)

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    # Generate scores
    X = df[feature_cols]
    X_scaled = scaler.transform(X)
    df['churn_probability'] = model.predict_proba(X_scaled)[:, 1]
    df['churn_risk'] = pd.cut(
        df['churn_probability'],
        bins=[0, 0.33, 0.66, 1.0],
        labels=['Low', 'Medium', 'High']
    )

    # Save results
    output_cols = [
        'user_id', 'email', 'full_name', 'plan',
        'events_total', 'had_return_visit', 'is_premium',
        'churn_probability', 'churn_risk', 'last_event_at'
    ]
    result = df[output_cols].sort_values('churn_probability', ascending=False)
    result.to_csv('analytics/churn/churn_scores.csv', index=False)

    print(f"Churn scores generated for {len(result)} users")
    print(f"\nRisk distribution:")
    print(result['churn_risk'].value_counts())
    print(f"\nTop 10 highest churn risk users:")
    print(result.head(10)[['user_id', 'email', 'plan',
                            'churn_probability', 'churn_risk']].to_string(index=False))

    return result


if __name__ == "__main__":
    predict_churn()