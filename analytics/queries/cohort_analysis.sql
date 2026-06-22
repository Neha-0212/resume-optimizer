-- Business question: Do newer users behave better than older ones?


WITH user_cohort AS (
    SELECT
        user_id,
        DATE_TRUNC('week', MIN(created_at)) AS cohort_week
    FROM events
    WHERE event_name = 'signup_completed'
    GROUP BY user_id
),
user_actions AS (
    SELECT
        uc.user_id,
        uc.cohort_week,
        MAX(CASE WHEN e.event_name = 'resume_uploaded' THEN 1 ELSE 0 END)              AS did_upload,
        MAX(CASE WHEN e.event_name = 'ats_analysis_completed' THEN 1 ELSE 0 END)       AS did_ats,
        MAX(CASE WHEN e.event_name = 'skill_gap_viewed' THEN 1 ELSE 0 END)             AS did_skill_gap,
        MAX(CASE WHEN e.event_name = 'premium_clicked' THEN 1 ELSE 0 END)              AS did_premium
    FROM user_cohort uc
    LEFT JOIN events e ON uc.user_id = e.user_id
    GROUP BY uc.user_id, uc.cohort_week
)
SELECT
    cohort_week::date                                               AS cohort,
    COUNT(*)                                                        AS total_users,
    ROUND(AVG(did_upload)   * 100, 1)                             AS upload_rate_pct,
    ROUND(AVG(did_ats)      * 100, 1)                             AS ats_rate_pct,
    ROUND(AVG(did_skill_gap)* 100, 1)                             AS skill_gap_rate_pct,
    ROUND(AVG(did_premium)  * 100, 1)                             AS premium_click_rate_pct
FROM user_actions
GROUP BY cohort_week
ORDER BY cohort_week DESC;