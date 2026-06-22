import streamlit as st
import os

# Mixpanel setup — fails silently if token missing
try:
    from mixpanel import Mixpanel
    _mp_token = os.getenv("MIXPANEL_TOKEN", "")
    _mp = Mixpanel(_mp_token) if _mp_token else None
    def track(user_id, event_name, props=None):
        if _mp:
            try:
                _mp.track(str(user_id), event_name, props or {})
            except Exception:
                pass
except Exception:
    def track(user_id, event_name, props=None):
        pass

st.set_page_config(
    page_title="Resume Optimizer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# Sidebar navigation
st.sidebar.title("Resume Optimizer")
st.sidebar.markdown("---")

if st.session_state.user_id:
    st.sidebar.success(f"Logged in as {st.session_state.user_name}")
    if st.sidebar.button("Logout"):
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.session_state.analysis_result = None
        st.rerun()

page = st.sidebar.radio(
    "Navigate",
    ["Home", "Upload & Analyze", "ATS Results", "Skill Gap", "Feedback"]
)

st.sidebar.markdown("---")
st.sidebar.caption("AI Resume Optimizer v1.0")

# ─── HOME PAGE ───────────────────────────────────────────────
if page == "Home":
    st.title("AI Resume Optimizer")
    st.subheader("Get your resume past ATS systems and land more interviews.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ATS Pass Rate", "73%", "+12% with optimization")
    with col2:
        st.metric("Skills Analyzed", "80+", "Technical + Product")
    with col3:
        st.metric("Interview Questions", "7", "Per analysis")

    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("""
    1. **Sign up or log in** using the Upload & Analyze page
    2. **Upload your resume** (PDF, DOCX, or TXT)
    3. **Paste a job description** you want to apply for
    4. **Get your ATS score**, skill gap, and interview questions instantly
    5. **Submit feedback** to help us improve
    """)

    st.info("Go to **Upload & Analyze** in the sidebar to get started.")

# ─── UPLOAD & ANALYZE PAGE ───────────────────────────────────
elif page == "Upload & Analyze":
    import requests

    st.title("Upload Resume & Analyze")
    st.markdown("---")

    # Login/Signup section
    if not st.session_state.user_id:
        st.subheader("Step 1: Login or Sign Up")
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login"):
                if email and password:
                    try:
                        res = requests.post(
                            "https://resume-optimizer-api.onrender.com/auth/login",
                            json={"email": email, "password": password}
                        )
                        if res.status_code == 200:
                            data = res.json()
                            st.session_state.user_id = data["user_id"]
                            st.session_state.user_name = data["full_name"]
                            st.success(f"Welcome back, {data['full_name']}!")
                            st.rerun()
                        else:
                            st.error(res.json().get("detail", "Login failed."))
                    except Exception as e:
                        st.error(f"Cannot connect to backend: {e}")
                else:
                    st.warning("Enter both email and password.")

        with tab2:
            new_name = st.text_input("Full Name", key="signup_name")
            new_email = st.text_input("Email", key="signup_email")
            new_pass = st.text_input("Password", type="password", key="signup_pass")
            if st.button("Create Account"):
                if new_name and new_email and new_pass:
                    try:
                        res = requests.post(
                            "https://resume-optimizer-api.onrender.com/auth/signup",
                            json={
                                "email": new_email,
                                "full_name": new_name,
                                "password": new_pass
                            }
                        )
                        if res.status_code == 201:
                            st.success("Account created. Please login.")
                        else:
                            st.error(res.json().get("detail", "Signup failed."))
                    except Exception as e:
                        st.error(f"Cannot connect to backend: {e}")
                else:
                    st.warning("Fill in all fields.")
    else:
        # Upload and analyze section
        st.subheader(f"Step 2: Upload Resume")
        st.info(f"Analyzing as user: **{st.session_state.user_name}**")

        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=["pdf", "docx", "txt"],
            help="Supported formats: PDF, DOCX, TXT. Max 5MB."
        )

        st.subheader("Step 3: Paste Job Description")
        job_title = st.text_input(
            "Job Title",
            placeholder="e.g. Senior Product Manager"
        )
        job_description = st.text_area(
            "Job Description",
            placeholder="Paste the full job description here...",
            height=200
        )

        if st.button("Analyze Resume", type="primary"):
            if not uploaded_file:
                st.warning("Please upload a resume file.")
            elif not job_title:
                st.warning("Please enter the job title.")
            elif not job_description or len(job_description) < 50:
                st.warning("Please paste a job description (at least 50 characters).")
            else:
                with st.spinner("Analyzing your resume..."):
                    try:
                        files = {"file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                        )}
                        data = {
                            "user_id": str(st.session_state.user_id),
                            "job_title": job_title,
                            "job_description": job_description
                        }
                        res = requests.post(
                            "https://resume-optimizer-api.onrender.com/resume/analyze",
                            files=files,
                            data=data
                        )
                        if res.status_code == 200:
                            st.session_state.analysis_result = res.json()
                            st.success("Analysis complete! Go to ATS Results in the sidebar.")
                            st.balloons()
                        else:
                            st.error(f"Analysis failed: {res.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Cannot connect to backend: {e}")

# ─── ATS RESULTS PAGE ────────────────────────────────────────
elif page == "ATS Results":
    st.title("ATS Score Results")
    st.markdown("---")

    result = st.session_state.analysis_result

    if not result:
        st.warning("No analysis results yet. Go to Upload & Analyze first.")
    else:
        # Score display
        score = result["ats_score"]
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("ATS Score", f"{score}/100")
        with col2:
            st.metric(
                "Keyword Match",
                f"{result['ats_details']['keyword_match_score']}%"
            )
        with col3:
            st.metric(
                "Semantic Match",
                f"{result['ats_details']['semantic_similarity_score']}%"
            )

        # Score interpretation
        st.markdown("---")
        if score >= 80:
            st.success(f"Strong Match — Your resume is well-aligned with this role.")
        elif score >= 60:
            st.warning(f"Moderate Match — Some gaps to address before applying.")
        else:
            st.error(f"Weak Match — Significant work needed before applying.")

        # Matched keywords
        st.subheader("Matched Keywords")
        keywords = result["ats_details"]["matched_keywords"]
        if keywords:
            cols = st.columns(5)
            for i, kw in enumerate(keywords):
                cols[i % 5].success(f"✓ {kw}")

        # Recommendations
        st.markdown("---")
        st.subheader("Recommendations")
        for rec in result["recommendations"]:
            st.info(f"💡 {rec}")

# ─── SKILL GAP PAGE ──────────────────────────────────────────
elif page == "Skill Gap":
    st.title("Skill Gap Analysis")
    st.markdown("---")

    result = st.session_state.analysis_result

    if not result:
        st.warning("No analysis results yet. Go to Upload & Analyze first.")
    else:
        skill_gap = result["skill_gap"]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Skills Match", f"{skill_gap['match_percentage']}%")
        with col2:
            st.metric("Missing Skills", len(skill_gap["missing_skills"]))

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Skills You Have")
            for skill in skill_gap["matched_skills"]:
                st.success(f"✓ {skill}")

        with col2:
            st.subheader("❌ Skills to Add")
            if skill_gap["missing_skills"]:
                for skill in skill_gap["missing_skills"]:
                    st.error(f"✗ {skill}")
            else:
                st.success("No missing skills found!")

        st.markdown("---")
        st.subheader("Interview Questions to Prepare")
        for i, q in enumerate(result["interview_questions"], 1):
            with st.expander(f"Q{i}: {q['skill'].title()} — {q['type'].replace('_', ' ').title()}"):
                st.write(q["question"])

# ─── FEEDBACK PAGE ───────────────────────────────────────────
elif page == "Feedback":
    import requests

    st.title("Submit Feedback")
    # Premium upsell — tracks who clicks upgrade
    if st.session_state.user_id and st.session_state.get("user_plan") == "free":
        st.markdown("---")
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown("**Upgrade to Premium** — Unlimited analyses, priority support.")
        with col2:
            if st.button("Upgrade →", type="primary"):
                try:
                    requests.post(
                        "https://resume-optimizer-api.onrender.com/feedback/submit",
                        json={
                            "user_id": st.session_state.user_id,
                            "feedback_text": "User clicked premium upgrade button",
                            "rating": None
                        }
                    )
                except:
                    pass
                # track("str(st.session_state.user_id)", "premium_clicked", {
                track(str(st.session_state.user_id), "premium_clicked", {
                    "source": "feedback_page",
                    "current_plan": "free"
                })
                st.info("Premium coming soon. We'll notify you.")
        # st.markdown("---")
    st.markdown("---")
    
    st.write("Help us improve the Resume Optimizer.")

    rating = st.slider("Rate your experience", 1, 5, 4)
    feedback_text = st.text_area(
        "Your feedback",
        placeholder="What worked well? What could be improved?",
        height=150
    )

    if st.button("Submit Feedback", type="primary"):
        if not feedback_text or len(feedback_text) < 10:
            st.warning("Please write at least 10 characters of feedback.")
        else:
            try:
                payload = {
                    "feedback_text": feedback_text,
                    "rating": rating
                }
                if st.session_state.user_id:
                    payload["user_id"] = st.session_state.user_id

                res = requests.post(
                    "https://resume-optimizer-api.onrender.com/feedback/submit",
                    json=payload
                )
                if res.status_code == 200:
                    st.success("Feedback submitted. Thank you.")
                else:
                    st.error("Submission failed. Try again.")
            except Exception as e:
                st.error(f"Cannot connect to backend: {e}")
