
# CareerMatch AI 🤖

An AI-powered Resume and Job Matching System built with Python and Streamlit. This project helps users analyze their resumes against job descriptions and understand how well their skills match a target role.

## ✨ Features

- 📄 Upload resumes in PDF, DOCX, and TXT formats
- 🎯 Compare resume content with a job description
- 📊 View a resume-job match score
- 🧠 Identify matched and missing skills
- 📜 Save and review previous analyses
- 👤 Manage a basic user profile
- 🗄️ Store analysis history using SQLite

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- SQLite
- PyPDF
- python-docx

## 📁 Project Structure

```text
CareerMatch-AI/
├── app.py
├── matching.py
├── db.py
├── style.css
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Duam123/CareerMatch-AI.git
cd CareerMatch-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application should open in your browser.

## 💡 How It Works

1. Upload your resume.
2. Enter a job title and job description.
3. Run the matching analysis.
4. Review the match score and skills identified by the application.
5. Check your previous analyses in the history section.

## 🔒 Security

- Do not upload API keys, passwords, or `.env` files.
- Local databases and virtual environment files should remain excluded through `.gitignore`.
- Resume matching results are intended as guidance and should not be treated as a definitive hiring decision.

## 👩‍💻 Author

**Dua Mirani**

- GitHub: [Duam123](https://github.com/Duam123)
- LinkedIn: [Connect on LinkedIn](https://www.linkedin.com/in/dua-mirani-a4468025b/)

---

⭐ If you find this project interesting, feel free to explore the code and share feedback.
