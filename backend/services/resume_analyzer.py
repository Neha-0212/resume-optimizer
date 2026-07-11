import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx
import io

# Load spacy model
nlp = spacy.load("en_core_web_sm")

# ─── SKILL LIBRARY ───────────────────────────────────────────
# These are the skills the engine knows about.
# Expandable — just add more terms.

TECHNICAL_SKILLS = [
    "python", "sql", "excel", "tableau", "power bi", "r", "java", "javascript",
    "html", "css", "react", "node", "django", "fastapi", "flask", "aws", "azure",
    "gcp", "docker", "kubernetes", "git", "postgresql", "mysql", "mongodb",
    "spark", "hadoop", "airflow", "dbt", "looker", "snowflake", "pandas",
    "numpy", "scikit-learn", "tensorflow", "pytorch", "machine learning",
    "deep learning", "nlp", "natural language processing", "computer vision",
    "statistics", "linear regression", "logistic regression", "xgboost",
    "a/b testing", "hypothesis testing", "data wrangling", "etl", "api"
]

PRODUCT_SKILLS = [
    "product management", "product roadmap", "user research", "wireframing",
    "prototyping", "figma", "jira", "confluence", "agile", "scrum", "kanban",
    "okr", "kpi", "metrics", "funnel analysis", "cohort analysis", "retention",
    "churn", "user stories", "sprint planning", "backlog", "prioritization",
    "go to market", "gtm", "competitive analysis", "market research",
    "stakeholder management", "product strategy", "product analytics",
    "growth hacking", "feature adoption", "user journey", "customer discovery"
]

SOFT_SKILLS = [
    "communication", "leadership", "teamwork", "problem solving",
    "critical thinking", "time management", "adaptability", "collaboration",
    "presentation", "negotiation", "project management", "decision making"
]

ALL_SKILLS = TECHNICAL_SKILLS + PRODUCT_SKILLS + SOFT_SKILLS


# ─── TEXT EXTRACTION ─────────────────────────────────────────

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def extract_text_from_docx(file_bytes: bytes) -> str:
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"


def extract_text_from_txt(file_bytes: bytes) -> str:
    try:
        return file_bytes.decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return f"Error reading TXT: {str(e)}"


def extract_resume_text(file_bytes: bytes, content_type: str) -> str:
    if "pdf" in content_type:
        return extract_text_from_pdf(file_bytes)
    elif "docx" in content_type or "wordprocessingml" in content_type:
        return extract_text_from_docx(file_bytes)
    else:
        return extract_text_from_txt(file_bytes)


# ─── SKILL EXTRACTION ────────────────────────────────────────

def extract_skills(text: str) -> list:
    text_lower = text.lower()
    found = []
    for skill in ALL_SKILLS:
        if skill.lower() in text_lower:
            found.append(skill)
    return list(set(found))


# ─── ATS SCORE ───────────────────────────────────────────────

def calculate_ats_score(resume_text: str, job_description: str) -> dict:
    """
    ATS score is calculated using two signals:
    1. Keyword overlap between resume and JD (60% weight)
    2. Cosine similarity of TF-IDF vectors (40% weight)

    Why two signals?
    - Keyword overlap catches exact matches (what basic ATS systems do)
    - Cosine similarity catches semantic relevance (what modern ATS systems do)
    """
    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()

    # Signal 1: Keyword overlap
    jd_words = set(re.findall(r'\b\w+\b', jd_lower))
    resume_words = set(re.findall(r'\b\w+\b', resume_lower))

    # Remove common stop words
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at",
                  "to", "for", "of", "with", "by", "from", "is", "are",
                  "was", "were", "be", "been", "have", "has", "had", "will",
                  "would", "could", "should", "may", "might", "do", "does",
                  "did", "not", "no", "your", "our", "their", "this", "that"}

    jd_keywords = jd_words - stop_words
    matched_keywords = jd_keywords.intersection(resume_words)

    keyword_score = (len(matched_keywords) / len(jd_keywords) * 100) if jd_keywords else 0
    keyword_score = min(keyword_score, 100)

    # Signal 2: Cosine similarity
    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=200)
        tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        similarity_score = similarity * 100
    except Exception:
        similarity_score = 0

    # Weighted final score
    final_score = (keyword_score * 0.6) + (similarity_score * 0.4)
    final_score = round(min(final_score, 100), 1)

    return {
        "ats_score": final_score,
        "keyword_match_score": round(keyword_score, 1),
        "semantic_similarity_score": round(similarity_score, 1),
        "matched_keywords": list(matched_keywords)[:20],
        "total_jd_keywords": len(jd_keywords),
        "total_matched": len(matched_keywords)
    }


# ─── SKILL GAP ANALYSIS ──────────────────────────────────────

def analyze_skill_gap(resume_text: str, job_description: str) -> dict:
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(job_description))

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills
    extra = resume_skills - jd_skills

    return {
        "skills_in_resume": sorted(list(resume_skills)),
        "skills_required_in_jd": sorted(list(jd_skills)),
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing)),
        "extra_skills": sorted(list(extra)),
        "match_percentage": round(
            len(matched) / len(jd_skills) * 100 if jd_skills else 0, 1
        )
    }


# ─── INTERVIEW QUESTIONS ─────────────────────────────────────

def generate_interview_questions(job_description: str, missing_skills: list) -> list:
    """
    Generates targeted interview questions based on:
    1. Skills mentioned in JD
    2. Skills missing from resume (highest priority — these are the gaps)
    """
    questions = []

    # Questions for missing skills (prepare for these)
    for skill in missing_skills[:3]:
        questions.append({
            "type": "skill_gap",
            "skill": skill,
            "question": f"Can you describe your experience with {skill}? "
                       f"Have you worked on any projects involving {skill}?"
        })

    # General product/analytical questions based on JD keywords
    jd_lower = job_description.lower()

    if any(word in jd_lower for word in ["product", "roadmap", "strategy"]):
        questions.append({
            "type": "product",
            "skill": "product thinking",
            "question": "Walk me through how you would prioritize features on a product roadmap with limited engineering resources."
        })

    if any(word in jd_lower for word in ["data", "analytics", "metrics", "sql"]):
        questions.append({
            "type": "analytical",
            "skill": "data analysis",
            "question": "How would you measure the success of a newly launched feature? What metrics would you track and why?"
        })

    if any(word in jd_lower for word in ["growth", "retention", "churn", "user"]):
        questions.append({
            "type": "growth",
            "skill": "growth thinking",
            "question": "If user retention dropped 15% month over month, how would you diagnose the problem and what would your action plan be?"
        })

    if any(word in jd_lower for word in ["stakeholder", "cross-functional", "communication"]):
        questions.append({
            "type": "behavioral",
            "skill": "stakeholder management",
            "question": "Tell me about a time you had to align multiple stakeholders with conflicting priorities. What was your approach?"
        })

    if any(word in jd_lower for word in ["agile", "scrum", "sprint"]):
        questions.append({
            "type": "process",
            "skill": "agile",
            "question": "How do you handle scope creep during a sprint? Describe a specific situation."
        })

    return questions[:7]


# ─── MASTER ANALYSIS FUNCTION ────────────────────────────────

def analyze_resume(
    file_bytes: bytes,
    content_type: str,
    job_description: str,
    job_title: str = ""
) -> dict:
    # Step 1: Extract text
    resume_text = extract_resume_text(file_bytes, content_type)

    if not resume_text or len(resume_text) < 50:
        return {"error": "Could not extract enough text from the resume file."}

    # Step 2: ATS score
    ats_result = calculate_ats_score(resume_text, job_description)

    # Step 3: Skill gap
    skill_gap = analyze_skill_gap(resume_text, job_description)

    # Step 4: Interview questions
    questions = generate_interview_questions(
        job_description,
        skill_gap["missing_skills"]
    )

    # Step 5: Simple recommendations
    # recommendations = []
    # if ats_result["ats_score"] < 50:
    #     recommendations.append("Your resume has low keyword match. Add more terms directly from the job description.")
    # if ats_result["ats_score"] < 70:
    #     recommendations.append("Tailor your resume summary section to mirror the language in the job description.")
    # if len(skill_gap["missing_skills"]) > 3:
    #     recommendations.append(f"You are missing {len(skill_gap['missing_skills'])} skills from the JD. Prioritize: {', '.join(skill_gap['missing_skills'][:3])}.")
    # if ats_result["ats_score"] >= 80:
    #     recommendations.append("Strong match. Focus on quantifying your achievements with numbers and impact.")

    recommendations = []

    if ats_result["ats_score"] < 50:
        recommendations.append(
            "Your resume has low keyword match. Add more terms directly from the job description."
        )

    if ats_result["ats_score"] < 75:
        recommendations.append(
            "Tailor your resume summary section to mirror the language in the job description."
        )

    if len(skill_gap["missing_skills"]) > 0:
        recommendations.append(
            f"You are missing {len(skill_gap['missing_skills'])} skills from the JD. Prioritize: {', '.join(skill_gap['missing_skills'])}."
        )

    if ats_result["ats_score"] >= 80:
        recommendations.append(
            "Strong match. Focus on quantifying your achievements with numbers and impact."
        )

    return {
        "job_title": job_title,
        "resume_text_length": len(resume_text),
        "ats_score": ats_result["ats_score"],
        "ats_details": ats_result,
        "skill_gap": skill_gap,
        "interview_questions": questions,
        "recommendations": recommendations
    }