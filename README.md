# 🧠 AI Resume Analyzer (Streamlit App)

An AI-based Python application that analyzes resumes, extracts key skills and experiences, and compares them with job descriptions to generate compatibility scores and insights.

---

## 🚀 Features

- 📄 **Upload Files Easily** — Supports both PDF and DOCX formats for resumes and job descriptions.  
- 🧩 **Text Extraction** — Automatically extracts textual content using `PyPDF2` and `python-docx`.  
- 🤖 **AI-Powered Similarity** — Uses **TF-IDF Vectorization** and **Cosine Similarity** to compute how closely a resume matches the job requirements.  
- 🧠 **Skill Matching** — Detects common technical and soft skills (like Python, SQL, ML, Communication, etc.) and compares them between resume and job description.  
- 📊 **Smart Insights** — Displays:
  - ✅ Matched Skills  
  - ⚠️ Missing Skills  
  - 💡 Extra Resume Skills  
- 🧾 **Clean Streamlit Interface** — Interactive web app with progress indicators and detailed results.

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Framework:** Streamlit  
- **Libraries:**
  - `PyPDF2` — For extracting text from PDF resumes  
  - `python-docx` — For DOCX text extraction  
  - `scikit-learn` — For TF-IDF and cosine similarity  
  - `re`, `pandas`, `numpy` (if used)  
  - `streamlit` — For the user interface  

---

## ⚙️ Installation & Setup

Follow these steps to run the **AI Resume Analyzer** app on your local machine.

---

### 🧩 1. Prerequisites

Before you begin, make sure you have:

- **Python 3.8 or higher** installed → [Download Python](https://www.python.org/downloads/)  
- **pip** (comes with Python)  
- **Git** (for cloning the repository)  
- Optional: a **virtual environment** tool like `venv` or `conda`

Install dependencies:
```bash
pip install streamlit PyPDF2 python-docx scikit-learn

### 1️⃣ **Run the app**
streamlit run app.py
After a few seconds, Streamlit will open your app automatically in your browser.
If it doesn’t, open this link manually:

👉 http://localhost:8501

🧠 6. Using the App

Upload a Job Description file (PDF/DOCX).

Upload a Resume file (PDF/DOCX).

Click on “Analyze & Score”.

View:

✅ Match Score (Similarity %)

🧩 Matched Skills

⚠️ Missing Skills

💡 Extra Resume Skills

👨‍💻 Author
  Khushal Jain
  Python and AI Enthusiast
  Passionate about building tools that combine AI and automation for smarter solutions to manual work
