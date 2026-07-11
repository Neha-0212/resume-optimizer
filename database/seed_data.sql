-- ============================================================
-- Seed Data for Testing
-- Simulates 30 days of user activity for analytics testing
-- ============================================================

-- Insert test users (passwords are hashed versions of "password123")
INSERT INTO users (email, full_name, hashed_password, plan, created_at) VALUES
('neha@test.com',    'Neha Sharma',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGTk9bMpBo9pFq8mV7Qz.kR3K2a', 'premium', NOW() - INTERVAL '30 days'),
('amit@test.com',    'Amit Patel',    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGTk9bMpBo9pFq8mV7Qz.kR3K2a', 'free',    NOW() - INTERVAL '25 days'),
('sara@test.com',    'Sara Khan',     '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGTk9bMpBo9pFq8mV7Qz.kR3K2a', 'free',    NOW() - INTERVAL '20 days'),
('ravi@test.com',    'Ravi Menon',    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGTk9bMpBo9pFq8mV7Qz.kR3K2a', 'premium', NOW() - INTERVAL '15 days'),
('priya@test.com',   'Priya Nair',    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGTk9bMpBo9pFq8mV7Qz.kR3K2a', 'free',    NOW() - INTERVAL '10 days'),
('john@test.com',    'John D''souza', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGTk9bMpBo9pFq8mV7Qz.kR3K2a', 'free',    NOW() - INTERVAL '8 days'),
('meena@test.com',   'Meena Iyer',   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGTk9bMpBo9pFq8mV7Qz.kR3K2a', 'free',    NOW() - INTERVAL '5 days'),
('carlos@test.com',  'Carlos Lima',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGTk9bMpBo9pFq8mV7Qz.kR3K2a', 'premium', NOW() - INTERVAL '3 days'),
('aisha@test.com',   'Aisha Malik',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGTk9bMpBo9pFq8mV7Qz.kR3K2a', 'free',    NOW() - INTERVAL '2 days'),
('dev@test.com',     'Dev Bose',     '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGTk9bMpBo9pFq8mV7Qz.kR3K2a', 'free',    NOW() - INTERVAL '1 day');

-- Insert sessions
INSERT INTO sessions (user_id, session_start, session_end, duration_seconds, device, source) VALUES
(1, NOW() - INTERVAL '30 days', NOW() - INTERVAL '30 days' + INTERVAL '12 minutes', 720,  'desktop', 'google'),
(1, NOW() - INTERVAL '20 days', NOW() - INTERVAL '20 days' + INTERVAL '8 minutes',  480,  'desktop', 'direct'),
(1, NOW() - INTERVAL '10 days', NOW() - INTERVAL '10 days' + INTERVAL '15 minutes', 900,  'mobile',  'linkedin'),
(2, NOW() - INTERVAL '25 days', NOW() - INTERVAL '25 days' + INTERVAL '5 minutes',  300,  'desktop', 'google'),
(2, NOW() - INTERVAL '12 days', NOW() - INTERVAL '12 days' + INTERVAL '4 minutes',  240,  'mobile',  'direct'),
(3, NOW() - INTERVAL '20 days', NOW() - INTERVAL '20 days' + INTERVAL '3 minutes',  180,  'desktop', 'google'),
(4, NOW() - INTERVAL '15 days', NOW() - INTERVAL '15 days' + INTERVAL '20 minutes', 1200, 'desktop', 'linkedin'),
(4, NOW() - INTERVAL '5 days',  NOW() - INTERVAL '5 days'  + INTERVAL '10 minutes', 600,  'desktop', 'direct'),
(5, NOW() - INTERVAL '10 days', NOW() - INTERVAL '10 days' + INTERVAL '6 minutes',  360,  'mobile',  'google'),
(6, NOW() - INTERVAL '8 days',  NOW() - INTERVAL '8 days'  + INTERVAL '2 minutes',  120,  'mobile',  'direct'),
(7, NOW() - INTERVAL '5 days',  NOW() - INTERVAL '5 days'  + INTERVAL '7 minutes',  420,  'desktop', 'google'),
(8, NOW() - INTERVAL '3 days',  NOW() - INTERVAL '3 days'  + INTERVAL '18 minutes', 1080, 'desktop', 'linkedin'),
(9, NOW() - INTERVAL '2 days',  NOW() - INTERVAL '2 days'  + INTERVAL '4 minutes',  240,  'mobile',  'google'),
(10,NOW() - INTERVAL '1 day',   NOW() - INTERVAL '1 day'   + INTERVAL '3 minutes',  180,  'desktop', 'direct');

-- Insert events (this is your funnel data)
INSERT INTO events (user_id, event_name, event_properties, page, created_at) VALUES
-- User 1: completed full funnel
(1, 'signup_completed',           '{"method": "email"}',                              '/signup',       NOW() - INTERVAL '30 days'),
(1, 'resume_uploaded',            '{"file_type": "pdf", "file_size_kb": 245}',        '/upload',       NOW() - INTERVAL '30 days' + INTERVAL '2 minutes'),
(1, 'ats_analysis_completed',     '{"ats_score": 78, "job_title": "Product Manager"}','/results',      NOW() - INTERVAL '30 days' + INTERVAL '4 minutes'),
(1, 'skill_gap_viewed',           '{"skills_missing": 3}',                            '/skill-gap',    NOW() - INTERVAL '30 days' + INTERVAL '6 minutes'),
(1, 'interview_questions_generated','{"question_count": 5}',                          '/interview',    NOW() - INTERVAL '30 days' + INTERVAL '8 minutes'),
(1, 'premium_clicked',            '{"source": "skill_gap_page"}',                     '/pricing',      NOW() - INTERVAL '30 days' + INTERVAL '10 minutes'),
(1, 'return_visit',               '{"days_since_last_visit": 10}',                    '/upload',       NOW() - INTERVAL '20 days'),
(1, 'resume_uploaded',            '{"file_type": "pdf", "file_size_kb": 312}',        '/upload',       NOW() - INTERVAL '20 days' + INTERVAL '1 minute'),
(1, 'ats_analysis_completed',     '{"ats_score": 85, "job_title": "Senior PM"}',      '/results',      NOW() - INTERVAL '20 days' + INTERVAL '3 minutes'),

-- User 2: dropped after ATS
(2, 'signup_completed',           '{"method": "email"}',                              '/signup',       NOW() - INTERVAL '25 days'),
(2, 'resume_uploaded',            '{"file_type": "docx", "file_size_kb": 180}',       '/upload',       NOW() - INTERVAL '25 days' + INTERVAL '3 minutes'),
(2, 'ats_analysis_completed',     '{"ats_score": 55, "job_title": "Data Analyst"}',   '/results',      NOW() - INTERVAL '25 days' + INTERVAL '5 minutes'),
(2, 'return_visit',               '{"days_since_last_visit": 13}',                    '/upload',       NOW() - INTERVAL '12 days'),

-- User 3: dropped after signup (never uploaded)
(3, 'signup_completed',           '{"method": "google"}',                             '/signup',       NOW() - INTERVAL '20 days'),

-- User 4: premium user, high engagement
(4, 'signup_completed',           '{"method": "linkedin"}',                           '/signup',       NOW() - INTERVAL '15 days'),
(4, 'resume_uploaded',            '{"file_type": "pdf", "file_size_kb": 290}',        '/upload',       NOW() - INTERVAL '15 days' + INTERVAL '2 minutes'),
(4, 'ats_analysis_completed',     '{"ats_score": 91, "job_title": "Growth Manager"}', '/results',      NOW() - INTERVAL '15 days' + INTERVAL '4 minutes'),
(4, 'skill_gap_viewed',           '{"skills_missing": 1}',                            '/skill-gap',    NOW() - INTERVAL '15 days' + INTERVAL '6 minutes'),
(4, 'interview_questions_generated','{"question_count": 5}',                          '/interview',    NOW() - INTERVAL '15 days' + INTERVAL '8 minutes'),
(4, 'premium_clicked',            '{"source": "results_page"}',                       '/pricing',      NOW() - INTERVAL '15 days' + INTERVAL '10 minutes'),
(4, 'return_visit',               '{"days_since_last_visit": 10}',                    '/upload',       NOW() - INTERVAL '5 days'),
(4, 'resume_uploaded',            '{"file_type": "pdf", "file_size_kb": 275}',        '/upload',       NOW() - INTERVAL '5 days' + INTERVAL '1 minute'),

-- User 5: dropped after upload
(5, 'signup_completed',           '{"method": "email"}',                              '/signup',       NOW() - INTERVAL '10 days'),
(5, 'resume_uploaded',            '{"file_type": "pdf", "file_size_kb": 198}',        '/upload',       NOW() - INTERVAL '10 days' + INTERVAL '5 minutes'),

-- Users 6-10: various drop-off points
(6, 'signup_completed',           '{"method": "email"}',                              '/signup',       NOW() - INTERVAL '8 days'),
(7, 'signup_completed',           '{"method": "google"}',                             '/signup',       NOW() - INTERVAL '5 days'),
(7, 'resume_uploaded',            '{"file_type": "docx", "file_size_kb": 220}',       '/upload',       NOW() - INTERVAL '5 days' + INTERVAL '2 minutes'),
(7, 'ats_analysis_completed',     '{"ats_score": 63, "job_title": "BA"}',             '/results',      NOW() - INTERVAL '5 days' + INTERVAL '4 minutes'),
(8, 'signup_completed',           '{"method": "linkedin"}',                           '/signup',       NOW() - INTERVAL '3 days'),
(8, 'resume_uploaded',            '{"file_type": "pdf", "file_size_kb": 310}',        '/upload',       NOW() - INTERVAL '3 days' + INTERVAL '1 minute'),
(8, 'ats_analysis_completed',     '{"ats_score": 88, "job_title": "APM"}',            '/results',      NOW() - INTERVAL '3 days' + INTERVAL '3 minutes'),
(8, 'skill_gap_viewed',           '{"skills_missing": 2}',                            '/skill-gap',    NOW() - INTERVAL '3 days' + INTERVAL '5 minutes'),
(8, 'premium_clicked',            '{"source": "skill_gap_page"}',                     '/pricing',      NOW() - INTERVAL '3 days' + INTERVAL '7 minutes'),
(9, 'signup_completed',           '{"method": "email"}',                              '/signup',       NOW() - INTERVAL '2 days'),
(10,'signup_completed',           '{"method": "google"}',                             '/signup',       NOW() - INTERVAL '1 day'),
(10,'resume_uploaded',            '{"file_type": "pdf", "file_size_kb": 255}',        '/upload',       NOW() - INTERVAL '1 day' + INTERVAL '3 minutes');

-- Insert feedback
INSERT INTO feedback (user_id, feedback_text, rating, created_at) VALUES
(1, 'The ATS score really helped me understand what recruiters see. Would love more detailed keyword suggestions.', 5, NOW() - INTERVAL '28 days'),
(2, 'Score seems too low for my resume. Not sure the matching is accurate.', 2, NOW() - INTERVAL '24 days'),
(3, 'Signed up but could not figure out what to do next. The UI is confusing.', 1, NOW() - INTERVAL '19 days'),
(4, 'Excellent tool. The skill gap section is very useful for targeted job applications.', 5, NOW() - INTERVAL '14 days'),
(5, 'Works fine but the analysis takes too long to load.', 3, NOW() - INTERVAL '9 days'),
(7, 'Good concept. Interview questions feature needs more variety.', 4, NOW() - INTERVAL '4 days'),
(8, 'Really liked the breakdown by job description. Premium seems worth it.', 5, NOW() - INTERVAL '2 days');

-- Insert subscriptions
INSERT INTO subscriptions (user_id, plan, status, amount_paid, started_at) VALUES
(1, 'premium', 'active',    999.0, NOW() - INTERVAL '28 days'),
(2, 'free',    'active',    0.0,   NOW() - INTERVAL '25 days'),
(3, 'free',    'active',    0.0,   NOW() - INTERVAL '20 days'),
(4, 'premium', 'active',    999.0, NOW() - INTERVAL '13 days'),
(5, 'free',    'active',    0.0,   NOW() - INTERVAL '10 days'),
(6, 'free',    'active',    0.0,   NOW() - INTERVAL '8 days'),
(7, 'free',    'active',    0.0,   NOW() - INTERVAL '5 days'),
(8, 'premium', 'active',    999.0, NOW() - INTERVAL '1 day'),
(9, 'free',    'active',    0.0,   NOW() - INTERVAL '2 days'),
(10,'free',    'active',    0.0,   NOW() - INTERVAL '1 day');