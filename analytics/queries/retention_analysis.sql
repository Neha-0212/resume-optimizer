--  question: Who comes back after signing up?

-- Day 1, Day 7, Day 30 retention
WITH user_first_seen AS (
    SELECT
        user_id,
        MIN(created_at)::date AS signup_date
    FROM events
    WHERE event_name = 'signup_completed'
    GROUP BY user_id
),
user_return_visits AS (
    SELECT DISTINCT
        user_id,
        created_at::date AS visit_date
    FROM events
    WHERE event_name IN ('resume_uploaded', 'ats_analysis_completed', 'return_visit')
)
SELECT
    ufs.signup_date,
    COUNT(DISTINCT ufs.user_id)                                                    AS cohort_size,
    COUNT(DISTINCT CASE
        WHEN urv.visit_date = ufs.signup_date + 1 THEN ufs.user_id END)           AS day1_retained,
    COUNT(DISTINCT CASE
        WHEN urv.visit_date BETWEEN ufs.signup_date + 6
        AND ufs.signup_date + 8 THEN ufs.user_id END)                             AS day7_retained,
    COUNT(DISTINCT CASE
        WHEN urv.visit_date BETWEEN ufs.signup_date + 28
        AND ufs.signup_date + 32 THEN ufs.user_id END)                            AS day30_retained,
    ROUND(COUNT(DISTINCT CASE
        WHEN urv.visit_date = ufs.signup_date + 1
        THEN ufs.user_id END)::numeric / NULLIF(COUNT(DISTINCT ufs.user_id),0) * 100, 1) AS day1_pct,
    ROUND(COUNT(DISTINCT CASE
        WHEN urv.visit_date BETWEEN ufs.signup_date + 6
        AND ufs.signup_date + 8
        THEN ufs.user_id END)::numeric / NULLIF(COUNT(DISTINCT ufs.user_id),0) * 100, 1) AS day7_pct
FROM user_first_seen ufs
LEFT JOIN user_return_visits urv ON ufs.user_id = urv.user_id
GROUP BY ufs.signup_date
ORDER BY ufs.signup_date DESC
LIMIT 30;