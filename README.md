# AI Resume Optimizer & Product Intelligence Platform

A full-stack AI product built to demonstrate end-to-end product analytics, 
NLP-based resume analysis, and churn prediction — targeted at Product Analyst, 
Growth Analyst, and APM roles.

## Live Demo
- **Application:** https://resume-optimizer-ezdk7qmf6657ixe3afuvga.streamlit.app/
- **API:** https://resume-optimizer-api-toi2.onrender.com
- **API Docs:** https://resume-optimizer-api-toi2.onrender.com/docs

> Note: Backend runs on Render free tier. First load may take 30-60 seconds.

---

## What This Project Does

Users can:
- Upload a resume (PDF, DOCX, TXT)
- Get an ATS score against a job description
- See a skill gap analysis with matched and missing skills
- Generate targeted interview questions based on skill gaps
- Submit feedback

The platform tracks all user behavior and feeds it into:
- Funnel analysis
- Retention analysis
- Cohort analysis
- Feature adoption tracking
- Sentiment-based feedback intelligence
- Churn prediction model

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Database | PostgreSQL |
| NLP | spaCy, TextBlob, scikit-learn TF-IDF |
| ML | XGBoost, scikit-learn |
| Analytics | Mixpanel, SQL |
| Dashboard | Power BI |
| Deployment | Render (backend + DB), Streamlit Cloud (frontend) |
| Version Control | GitHub |

---

## Product Metrics (from Power BI Dashboard)

| Metric                  | Value                               |
| ----------------------- | ----------------------------------- |
| Total Users             | 103                                 |
| Premium Conversion Rate | 15.53%                              |
| Average User Rating     | 3.29 / 5                            |
| Churn Rate              | 38.83%                              |
| Biggest Funnel Drop-off | ATS Analysis → Skill Gap (68% drop) |
| Day 7 Retention         | ~45% average across cohorts         |

---

## Key Product Insights

### Funnel Performance

* Approximately 93% of users who sign up proceed to upload a resume.
* Only 32% of users who complete ATS analysis continue to view the Skill Gap page.
* The transition from ATS Analysis to Skill Gap represents the largest funnel drop-off, with approximately 68% of users abandoning the journey at this stage.
* Improving the visibility and perceived value of Skill Gap recommendations should be a major product priority.

### Churn Analysis

* Session count is the strongest predictor of churn, contributing approximately 49% of model importance.
* Users with only one session and no return visit within 14 days exhibit churn probabilities exceeding 97%.
* Free-plan users account for the majority of high-risk churn users.
* Increasing early engagement and encouraging repeat visits within the first week are likely to produce the greatest retention gains.

### Customer Feedback Insights

* User sentiment remains predominantly positive, with:

  * 60.4% Positive feedback
  * 27.1% Neutral feedback
  * 12.5% Negative feedback
* The overall average rating across feedback is approximately 3.29 out of 5.

### Areas Performing Well

* The **Features** category generated the largest volume of feedback (18 responses) and achieved the highest average sentiment score (0.530), indicating strong user appreciation for capabilities such as ATS analysis and skill gap recommendations.
* The **Accuracy** category also performed well, maintaining positive sentiment (0.282) with no negative feedback recorded.

### Primary User Pain Points

* **Performance** emerged as the most critical issue:

  * 5 out of 7 performance-related feedback entries were negative.
  * Despite an average rating of 3.00, the sentiment profile indicates significant frustration regarding application speed and responsiveness.
* **Onboarding** received the lowest rating (1.00) and recorded negative sentiment (-0.150), suggesting that some users experience difficulty understanding the product during their first interaction.

### Sentiment Trends

* Weekly sentiment remained consistently positive throughout the observation period, with average sentiment scores ranging from 0.225 to 0.448.
* Negative feedback appeared intermittently rather than increasing over time, indicating isolated usability issues rather than a widespread decline in product satisfaction.

### NLP Limitations

* The current sentiment pipeline relies on TextBlob sentiment analysis.
* TextBlob occasionally struggles with contextual language and negation handling (for example, phrases such as "not bad" or "not very useful"), which can lead to sentiment misclassification.
* Future production implementations should consider transformer-based models such as BERT or RoBERTa for improved sentiment accuracy.


## Architecture

```
User → Streamlit Frontend
         ↓
    FastAPI Backend
         ↓
    PostgreSQL DB ← SQLAlchemy ORM
         ↓
    Mixpanel (event tracking)
         ↓
    Power BI (dashboards via CSV export)
         ↓
    XGBoost Churn Model
```

---

## Project Structure

```
resume-optimizer/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Environment config
│   ├── database.py          # PostgreSQL connection
│   ├── models/              # SQLAlchemy models
│   ├── routes/              # API endpoints
│   ├── services/            # Resume analyzer, feedback NLP, Mixpanel
│   └── schemas/             # Pydantic request/response models
├── frontend/
│   └── app.py               # Streamlit UI
├── database/
│   ├── schema.sql           # Table definitions
│   └── seed_data.sql        # Test data
├── analytics/
│   ├── queries/             # SQL: funnel, retention, cohort, adoption
│   └── churn/               # XGBoost model training and 
|
└── exports/                 # CSV exports for Power BI
```

---

## Run Locally

### Prerequisites
- Python 3.11
- PostgreSQL 16
- Git

### Setup

**1. Clone the repository:**
```bash
git clone https://github.com/Neha-0212/resume-optimizer.git
cd resume-optimizer
```

**2. Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m textblob.download_corpora
```

**4. Configure environment:**
```bash
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/resume_optimizer
SECRET_KEY=your-secret-key
ENVIRONMENT=development
MIXPANEL_TOKEN=your-mixpanel-token
```

**5. Set up database:**
```bash
psql -U postgres -c "CREATE DATABASE resume_optimizer;"
psql -U postgres -d resume_optimizer -f database/schema.sql
psql -U postgres -d resume_optimizer -f database/seed_data.sql
python -m backend.create_tables
```

**6. Start PostgreSQL (Windows):**
```bash
"C:\Program Files\PostgreSQL\16\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\16\data" start
```

**7. Run backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**8. Run frontend (new terminal):**
```bash
streamlit run frontend/app.py
```

**9. Open:**
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs

### Test login credentials
```
Email: neha@test.com
Password: password123
```

---

## Run Analytics

**Feedback sentiment analysis:**
```bash
python -m analytics.run_feedback_analysis
```

**Train churn model:**
```bash
python -m analytics.churn.train_model
```

**Generate churn predictions:**
```bash
python -m analytics.churn.predict
```

**Export data for Power BI:**
```bash
psql -U postgres -d resume_optimizer -c "\COPY (SELECT * FROM users) TO 'exports/users.csv' CSV HEADER"
```

---
## Power BI Dashboard

The dashboard connects to exported CSV files from PostgreSQL and contains 6 pages covering the full product analytics story.

### Dashboard Pages

---

#### Page 1 — Executive Overview

![Executive Overview](screenshots/executive_overview.jpg)

> A single-screen summary of the product's health. Built for stakeholders who need the full picture in under 30 seconds without drilling into individual reports.

**What it shows:**
- Total users, premium conversion rate, average rating, and churn rate as KPI cards
- User distribution by plan (free vs premium) as a pie chart
- Monthly user growth trend as a line chart
- High churn user count by risk level as a bar chart

**Why it matters:** This is the first page any product leader or investor would open. If churn rate is high and premium rate is low, the business has a monetization problem. If avg rating is below 3.0, the product has a satisfaction problem. This page surfaces both at a glance.

---

#### Page 2 — Acquisition

![Acquisition](screenshots/acquisition.jpg)

> Tracks where users are coming from and how they arrive. Answers the question: which channels are actually working?

**What it shows:**
- Daily signup volume as a column chart
- Traffic source breakdown (Google, LinkedIn, Direct) as a pie chart
- Device split (desktop vs mobile) as a donut chart
- Plan distribution at signup as a bar chart

**Why it matters:** If 80% of users come from Google but LinkedIn users convert to premium at 3x the rate, you should invest in LinkedIn — not Google. Acquisition data without conversion context is misleading. This page connects source to behavior.

---

#### Page 3 — Funnel

![Funnel](screenshots/funnel_anlaysis.jpg)

> Maps the user journey from signup to premium click. Identifies exactly where users drop off and how many make it through each stage.

**What it shows:**
- 6-step funnel: Signup → Upload → ATS Analysis → Skill Gap → Interview Questions → Premium Click
- Signup-to-upload conversion rate as a KPI card
- Upload-to-ATS conversion rate as a KPI card
- Event volume over time as a line chart

**Key finding:** 93% of users upload a resume after signing up — strong activation. But only 32% view the skill gap after completing ATS analysis — the biggest drop-off in the product. This is the page that makes the case for redesigning the post-ATS experience.

**Why it matters:** Without a funnel, you're guessing where to improve. With it, you know exactly which step to fix first.

---

#### Page 4 — Retention

![Retention](screenshots/retention.jpg)

> Measures how often users come back after their first visit. Retention is the single most important signal of product-market fit.

**What it shows:**
- Return visit rate as a large KPI card
- Session count by device over time as a stacked bar chart
- Average session duration by traffic source as a bar chart
- Feature usage matrix by plan (free vs premium) as a table

**Why it matters:** A product with high acquisition but low retention has a leaky bucket problem — you're spending to acquire users you can't keep. This page shows whether the product creates habits or just one-time visits. LinkedIn users in this dataset show longer session durations, suggesting higher intent users arrive from professional channels.

---

#### Page 5 — Feedback

![Feedback](screenshots/feedback.jpg)

> Turns unstructured user text into structured product intelligence. Shows what users love, what frustrates them, and how sentiment changes over time.

**What it shows:**
- Sentiment breakdown (positive / neutral / negative) as a pie chart
- Average rating by feedback category as a bar chart
- Weekly sentiment score trend as a line chart
- Full feedback table sorted by lowest rating first

**Key finding:** Performance is the most critical problem — lowest avg rating at 2.29 and the highest concentration of negative sentiment. Features category has the most feedback volume but positive sentiment, meaning users want more features but aren't angry about the current ones.

**Why it matters:** Most products collect feedback but never analyze it systematically. This page shows how NLP can convert raw text into a prioritized list of product problems.

---

#### Page 6 — Churn

![Churn](screenshots/churn_analysis.jpg)

> Shows which users are at risk of leaving and how confident the model is about each prediction. Built to support proactive retention interventions.

**What it shows:**
- Churn risk distribution (Low / Medium / High) as a bar chart
- Churn risk breakdown by plan as a stacked bar chart
- Top high-risk users table sorted by churn probability
- Churn probability distribution as a histogram

**Key finding:** 38.83% of users are classified as high churn risk. Free plan users dominate this segment. Users with only one session and no return visit within 14 days show 97%+ churn probability. The histogram shows a U-shaped distribution — most users are either clearly retained or clearly churned, with few in the middle.

**Why it matters:** Without a churn model, retention efforts are reactive — you only know a user churned after they leave. This page enables proactive intervention: identify high-risk users before they leave and trigger targeted re-engagement.

---

### DAX Measures

Key measures built in the data model:

```dax
Total Users = COUNTROWS('users')
Premium Rate % = DIVIDE([Premium Users], [Total Users]) * 100
Churn Rate % = DIVIDE([High Churn Users], [Total Users]) * 100
Signup to Upload % = DIVIDE(
    CALCULATE(DISTINCTCOUNT(events[user_id]), events[event_name] = "resume_uploaded"),
    CALCULATE(DISTINCTCOUNT(events[user_id]), events[event_name] = "signup_completed")
) * 100
Return Visit Rate % = DIVIDE(
    CALCULATE(COUNTROWS(events), events[event_name] = "return_visit"),
    CALCULATE(COUNTROWS(events), events[event_name] = "signup_completed")
) * 100
```

### Data Model

- `users` is the center table
- `events`, `feedback`, `sessions`, `subscriptions` connect via `user_id` (Many-to-One)
- `churn_scores` connects via `user_id` (One-to-One)
- All relationships support cross-filtering across pages

### How to Refresh Data

**1. Export fresh data from PostgreSQL:**
```bash
psql -U postgres -d resume_optimizer -c "\COPY (SELECT id, email, full_name, plan, is_active, created_at FROM users) TO 'exports/users.csv' CSV HEADER"
psql -U postgres -d resume_optimizer -c "\COPY (SELECT id, user_id, event_name, page, created_at FROM events) TO 'exports/events.csv' CSV HEADER"
psql -U postgres -d resume_optimizer -c "\COPY (SELECT id, user_id, feedback_text, rating, sentiment, sentiment_score, category, created_at FROM feedback) TO 'exports/feedback.csv' CSV HEADER"
psql -U postgres -d resume_optimizer -c "\COPY (SELECT id, user_id, session_start, duration_seconds, device, source FROM sessions) TO 'exports/sessions.csv' CSV HEADER"
psql -U postgres -d resume_optimizer -c "\COPY (SELECT id, user_id, plan, status, amount_paid FROM subscriptions) TO 'exports/subscriptions.csv' CSV HEADER"
python -m analytics.churn.predict
copy analytics\churn\churn_scores.csv exports\churn_scores.csv
```

**2. In Power BI Desktop:**
- Click `Home` → `Refresh`
- All 6 pages update automatically

### File
The dashboard file `resume_optimizer.pbix` is available in the repository root.

## Known Limitations

- **Cold start:** Render free tier sleeps after 15 min inactivity. First request takes 30-60s.
- **Database expiry:** Render free PostgreSQL expires after 90 days.
- **Sentiment accuracy:** TextBlob misclassifies negated phrases. Production would use fine-tuned BERT.
- **Churn model:** Trained on synthetic data. AUC 0.894. Behavioral features need real user data to be meaningful.
- **Mixpanel:** City/country not tracked — server-side Python SDK does not auto-detect location.

---

## Author

Neha | Product Analyst Portfolio Project  
GitHub: https://github.com/Neha-0212
