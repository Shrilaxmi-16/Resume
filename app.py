import streamlit as st
import re
from PyPDF2 import PdfReader

# Predefined lists of skills and common education keywords
SKILLS_DB = [
    'Python', 'Java', 'SQL', 'Machine Learning', 'Data Science', 'Deep Learning', 
    'NLP', 'TensorFlow', 'Keras', 'Flask', 'Django', 'Pandas', 'NumPy', 'Matplotlib', 
    'Data Analysis', 'AI', 'AWS', 'GCP', 'Azure', 'Hadoop'
]

EDUCATION_DB = [
    'B.Sc', 'M.Sc', 'B.Tech', 'M.Tech', 'PhD', 'MBA', 'Bachelor', 'Master', 'Diploma', 'Degree'
]

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Function to extract contact details using regex
def extract_contact_details(text):
    email = re.findall(r'\S+@\S+', text)
    phone = re.findall(r'\b\d{10}\b', text)
    return email, phone

# Function to extract skills based on predefined list
def extract_skills(text):
    skills = [skill for skill in SKILLS_DB if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)]
    return skills

# Function to extract education details based on predefined list
def extract_education(text):
    education_details = [edu for edu in EDUCATION_DB if re.search(r'\b' + re.escape(edu) + r'\b', text, re.IGNORECASE)]
    return education_details

# Function to extract company names and experience
def extract_experience(text):
    companies = re.findall(r'\b\w+(?:\s\w+)*(?: Inc| LLC| Ltd| Technologies| Corp)\b', text)
    return companies

# Function to match resume with a job description (simplified)
def match_job_description(text, job_description):
    skills = extract_skills(text)
    job_skills = extract_skills(job_description)
    matched_skills = [skill for skill in skills if skill in job_skills]
    return len(matched_skills) / len(job_skills) if job_skills else 0

# Main Streamlit app
def main():
    st.title("Smart Resume Analyzer")
    
    st.write("Upload your resume in PDF format to extract and analyze relevant details.")
    
    pdf_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    
    if pdf_file:
        resume_text = extract_text_from_pdf(pdf_file)
        st.subheader("Extracted Resume Text:")
        st.write(resume_text)

        email, phone = extract_contact_details(resume_text)
        st.subheader("Contact Information:")
        st.write(f"Email: {', '.join(email) if email else 'No email found'}")
        st.write(f"Phone: {', '.join(phone) if phone else 'No phone number found'}")

        skills = extract_skills(resume_text)
        st.subheader("Extracted Skills:")
        st.write(", ".join(skills) if skills else "No skills found")

        experience = extract_experience(resume_text)
        st.subheader("Work Experience (Companies):")
        st.write(", ".join(experience) if experience else "No experience found")

        education = extract_education(resume_text)
        st.subheader("Education Details:")
        st.write(", ".join(education) if education else "No education details found")

        # Job Description Matching (optional)
        st.subheader("Job Description Matching")
        job_desc = st.text_area("Paste Job Description", "")
        if job_desc:
            match_score = match_job_description(resume_text, job_desc)
            st.write(f"Match Score: {match_score:.2%}")

if __name__ == "__main__":
    main()
