-- Business question: Which features are actually being used?

WITH total_users AS (
    SELECT COUNT(DISTINCT user_id) AS total FROM events
    WHERE event_name = 'signup_completed'
),
feature_usage AS (
    SELECT
        event_name                          AS feature,
        COUNT(DISTINCT user_id)             AS unique_users,
        COUNT(*)                            AS total_uses,
        ROUND(COUNT(*)::numeric /
            NULLIF(COUNT(DISTINCT user_id),0), 2) AS avg_uses_per_user
    FROM events
    WHERE event_name IN (
        'resume_uploaded',
        'ats_analysis_completed',
        'skill_gap_viewed',
        'interview_questions_generated',
        'premium_clicked',
        'feedback_submitted'
    )
    GROUP BY event_name
)
SELECT
    fu.feature,
    fu.unique_users,
    fu.total_uses,
    fu.avg_uses_per_user,
    ROUND(fu.unique_users::numeric / NULLIF(tu.total,0) * 100, 1) AS adoption_rate_pct
FROM feature_usage fu, total_users tu
ORDER BY adoption_rate_pct DESC;