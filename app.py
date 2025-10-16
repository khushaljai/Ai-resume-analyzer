import streamlit as st
import PyPDF2
from docx import Document
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. Utility Functions for Text Extraction ---

def extract_text_from_pdf(file):
    """Extracts text from a PDF file stream."""
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def extract_text_from_docx(file):
    """Extracts text from a DOCX file stream."""
    try:
        document = Document(file)
        text = ""
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
        return ""

def get_text_from_file(uploaded_file):
    """Determines file type and calls the appropriate extraction function."""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(uploaded_file)
    elif file_extension == 'docx':
        return extract_text_from_docx(uploaded_file)
    else:
        st.warning(f"Unsupported file type: {file_extension}")
        return ""

# --- 2. NLP and Skill Matching ---

# Basic list of skills (can be greatly expanded)
COMMON_SKILLS = [
    "python", "java", "c++", "javascript", "html", "css", "sql", "nosql",
    "machine learning", "deep learning", "nlp", "data science", "tableau",
    "power bi", "excel", "aws", "azure", "google cloud", "docker", "kubernetes",
    "git", "agile", "scrum", "project management", "communication", "leadership",
    "problem-solving", "critical thinking", "data analysis", "r"
]

def extract_matched_skills(text, skills_list):
    """
    Tokenizes text and finds matching skills from the predefined list.
    Returns a set of matched skills and the cleaned text.
    """
    # Clean text: lower case, remove punctuation, tokenize by space
    text = text.lower()
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    tokens = set(cleaned_text.split())
    
    # Identify skills present in the text
    matched_skills = set()
    for skill in skills_list:
        # Check for simple skill match
        if skill in tokens:
            matched_skills.add(skill)
        # Check for multi-word skill match (e.g., 'machine learning')
        elif skill in text:
            matched_skills.add(skill)
            
    return matched_skills, cleaned_text

# --- 3. Main Streamlit Application ---

st.set_page_config(page_title="Resume Analyzer ??", layout="wide")
st.title("Automated Resume Analyzer (HR Tool) ??")
st.markdown("Upload a Job Description and a Resume to get a similarity score and skill breakdown.")

# File Uploads
col1, col2 = st.columns(2)
with col1:
    job_description_file = st.file_uploader(
        "Upload **Job Description** (PDF/DOCX)", 
        type=["pdf", "docx"], 
        key="jd_uploader"
    )

with col2:
    resume_file = st.file_uploader(
        "Upload **Resume** (PDF/DOCX)", 
        type=["pdf", "docx"], 
        key="resume_uploader"
    )

if st.button("Analyze & Score", use_container_width=True):
    if job_description_file is None or resume_file is None:
        st.error("?? Please upload both the Job Description and the Resume to run the analysis.")
    else:
        with st.spinner("Analyzing documents..."):
            
            # --- Text Extraction ---
            jd_text = get_text_from_file(job_description_file)
            resume_text = get_text_from_file(resume_file)
            
            if not jd_text or not resume_text:
                st.error("Could not extract text from one or both files.")
                st.stop()
            
            # --- Skill Extraction & Pre-processing ---
            # Using the pre-defined list for skill matching
            jd_skills, jd_cleaned_text = extract_matched_skills(jd_text, COMMON_SKILLS)
            resume_skills, resume_cleaned_text = extract_matched_skills(resume_text, COMMON_SKILLS)
            
            # --- Similarity Calculation (Vectorization) ---
            
            # Use TfidfVectorizer to convert text into numerical vectors
            vectorizer = TfidfVectorizer(stop_words='english')
            
            # Fit and transform both documents
            tfidf_matrix = vectorizer.fit_transform([jd_cleaned_text, resume_cleaned_text])
            
            # Calculate Cosine Similarity between the two vectors
            # The result is a 2x2 matrix, we take the value at [0][1]
            similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to a percentage for display
            score_percent = f"{similarity_score * 100:.2f}%"

            # --- Display Results ---
            st.success("? Analysis Complete!")
            
            st.subheader("Match Score")
            st.metric(label="Resume Similarity to Job Description", value=score_percent)

            st.subheader("Skill Breakdown")
            
            # Sets for comparison
            matched_skills = jd_skills.intersection(resume_skills)
            missing_skills = jd_skills.difference(resume_skills)
            
            col_res1, col_res2, col_res3 = st.columns(3)
            
            with col_res1:
                st.info("?? **Matched Skills**")
                st.write(f"Count: **{len(matched_skills)}**")
                st.markdown(", ".join(f"**`{s.title()}`**" for s in sorted(list(matched_skills))))
                
            with col_res2:
                st.error("? **Missing Skills (Job Req)**")
                st.write(f"Count: **{len(missing_skills)}**")
                st.markdown(", ".join(f"`{s.title()}`" for s in sorted(list(missing_skills))))

            with col_res3:
                st.warning("?? **Extra Resume Skills**")
                extra_skills = resume_skills.difference(jd_skills)
                st.write(f"Count: **{len(extra_skills)}**")
                st.markdown(", ".join(f"`{s.title()}`" for s in sorted(list(extra_skills))))
                
            st.markdown("---")
            st.caption(
                "Note: The similarity score is based on the entire text content (TF-IDF), "
                "while the skill breakdown uses a basic keyword matching approach."
            )
