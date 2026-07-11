-- ============================================================
-- FUNNEL ANALYSIS
-- Business question: Where do users drop off?
-- ============================================================

WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event_name = 'signup_completed' THEN user_id END)              AS step1_signups,
        COUNT(DISTINCT CASE WHEN event_name = 'resume_uploaded' THEN user_id END)               AS step2_uploads,
        COUNT(DISTINCT CASE WHEN event_name = 'ats_analysis_completed' THEN user_id END)        AS step3_ats,
        COUNT(DISTINCT CASE WHEN event_name = 'skill_gap_viewed' THEN user_id END)              AS step4_skill_gap,
        COUNT(DISTINCT CASE WHEN event_name = 'interview_questions_generated' THEN user_id END) AS step5_interview,
        COUNT(DISTINCT CASE WHEN event_name = 'premium_clicked' THEN user_id END)               AS step6_premium
    FROM events
)
SELECT
    'Step 1: Signup'            AS funnel_step, step1_signups    AS users, 100.0                                          AS conversion_pct FROM funnel
UNION ALL
SELECT 'Step 2: Upload',         step2_uploads,  ROUND(step2_uploads::numeric  / NULLIF(step1_signups,0) * 100, 1) FROM funnel
UNION ALL
SELECT 'Step 3: ATS Analysis',   step3_ats,      ROUND(step3_ats::numeric      / NULLIF(step1_signups,0) * 100, 1) FROM funnel
UNION ALL
SELECT 'Step 4: Skill Gap',      step4_skill_gap,ROUND(step4_skill_gap::numeric/ NULLIF(step1_signups,0) * 100, 1) FROM funnel
UNION ALL
SELECT 'Step 5: Interview Qs',   step5_interview,ROUND(step5_interview::numeric/ NULLIF(step1_signups,0) * 100, 1) FROM funnel
UNION ALL
SELECT 'Step 6: Premium Click',  step6_premium,  ROUND(step6_premium::numeric  / NULLIF(step1_signups,0) * 100, 1) FROM funnel
ORDER BY funnel_step;