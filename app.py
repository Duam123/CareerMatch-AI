
import streamlit as st
import pandas as pd
from pathlib import Path
from pypdf import PdfReader
from docx import Document

import db
from matching import match_resume

st.set_page_config(
    page_title="CareerMatch AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = Path(__file__).parent / "style.css"
if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )

db.init_db()


def extract_text(uploaded_file):
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if name.endswith(".docx"):
        doc = Document(uploaded_file)
        return "\n".join(p.text for p in doc.paragraphs)

    if name.endswith(".txt"):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")

    return ""


def show_tags(items):
    if items:
        st.write(" · ".join(items))
    else:
        st.caption("No skills found.")


with st.sidebar:
    st.markdown("# 🎯 CareerMatch AI")
    st.caption("Your AI career assistant")
    st.divider()

    page = st.radio(
        "MAIN MENU",
        [
            "Dashboard",
            "Resume & Job Matching",
            "Analysis History",
            "My Profile",
        ],
    )

    st.divider()
    st.caption("AI-powered career insights")
    st.caption("Version 1.0")


if page == "Dashboard":
    stats = db.get_stats()
    recent = db.get_analyses(limit=5)

    st.title("Welcome back! 👋")
    st.write(
        "Find your next opportunity with AI-powered resume matching."
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("Resumes Analyzed", stats["total"])
    c2.metric("Average Match Score", f'{stats["average"]}%')
    c3.metric("Jobs Compared", stats["jobs"])

    st.write("")
    left, right = st.columns([1.5, 1])

    with left:
        st.subheader("Recent Activity")

        if recent:
            df = pd.DataFrame(
                recent,
                columns=[
                    "ID",
                    "Resume",
                    "Job Title",
                    "Match Score",
                    "Date",
                ],
            )
            st.dataframe(
                df[["Resume", "Job Title", "Match Score", "Date"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            with st.container(border=True):
                st.markdown("### ✨ Your journey starts here")
                st.write(
                    "Upload your resume and compare it with a job "
                    "description to see your matching skills."
                )
                if st.button("Start Matching", type="primary"):
                    st.session_state["go_matching"] = True
                    st.rerun()

    with right:
        st.subheader("Quick Start")
        with st.container(border=True):
            st.markdown("### 📄 Analyze your resume")
            st.write(
                "Discover matching skills, missing requirements "
                "and your overall skill match."
            )
            if st.button("Open Job Matching", use_container_width=True):
                st.session_state["go_matching"] = True
                st.rerun()

        st.subheader("Career Tip")
        st.info(
            "Tailor your resume to the requirements of each job. "
            "Include relevant skills and real project experience."
        )

elif page == "Resume & Job Matching" or st.session_state.pop(
    "go_matching", False
):
    st.title("Resume & Job Matching")
    st.write("Compare your resume with a job description.")

    uploaded = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx", "txt"],
    )

    job_title = st.text_input(
        "Job title",
        placeholder="e.g. Junior Python Developer",
    )

    job_description = st.text_area(
        "Job description",
        height=220,
        placeholder="Paste the job requirements here...",
    )

    if st.button("Analyze Resume", type="primary"):
        if not uploaded:
            st.error("Please upload your resume first.")
        elif not job_title.strip() or not job_description.strip():
            st.error("Please enter the job title and job description.")
        else:
            with st.spinner("Analyzing skills..."):
                resume_text = extract_text(uploaded)

                if not resume_text.strip():
                    st.error(
                        "No readable text found. Try a text-based PDF, "
                        "DOCX or TXT file."
                    )
                else:
                    report = match_resume(
                        resume_text, job_description
                    )

                    db.save_analysis(
                        uploaded.name,
                        job_title.strip(),
                        report["score"],
                    )

                    st.session_state["last_report"] = report
                    st.session_state["last_job_title"] = job_title.strip()
                    st.session_state["last_resume"] = uploaded.name

    report = st.session_state.get("last_report")

    if report:
        st.divider()
        st.subheader("Analysis Report")

        st.metric("Skill Match Score", f'{report["score"]}%')
        st.progress(int(report["score"]) / 100)

        good, missing = st.columns(2)

        with good:
            st.markdown("#### ✅ Matching Skills")
            show_tags(report["matched_skills"])

        with missing:
            st.markdown("#### 📌 Skills to Improve")
            show_tags(report["missing_skills"])

        st.caption(
            "This score is based on detected skills only; it is not "
            "a guarantee of job suitability."
        )

elif page == "Analysis History":
    st.title("Analysis History")
    st.write("Review your previous resume analyses.")

    rows = db.get_analyses()

    if rows:
        df = pd.DataFrame(
            rows,
            columns=[
                "ID",
                "Resume",
                "Job Title",
                "Match Score",
                "Date",
            ],
        )
        st.dataframe(df, use_container_width=True, hide_index=True)

        ids = [row[0] for row in rows]
        selected_id = st.selectbox("Select analysis ID to delete", ids)

        if st.button("Delete Selected Analysis"):
            db.delete_analysis(selected_id)
            st.success("Analysis deleted.")
            st.rerun()
    else:
        st.info("No analysis history yet. Analyze a resume first.")

elif page == "My Profile":
    st.title("My Profile")
    st.write("Add your career information.")

    with st.form("profile_form"):
        name = st.text_input("Full name")
        target = st.text_input(
            "Target role",
            placeholder="e.g. Software Engineer",
        )
        skills = st.text_area(
            "Your skills",
            placeholder="Python, React, SQL...",
        )

        submitted = st.form_submit_button("Save Profile")

        if submitted:
            st.session_state["profile"] = {
                "name": name,
                "target": target,
                "skills": skills,
            }
            st.success("Profile saved for this session.")
