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
