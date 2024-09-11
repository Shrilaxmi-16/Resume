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
        text += page.extract_text()
    return text

# Function to extract contact details using regex
def extract_contact_details(text):
    # Extracting email addresses
    email = re.findall(r'\S+@\S+', text)
    
    # Extracting phone numbers (10 digits)
    phone = re.findall(r'\b\d{10}\b', text)
    
    return email, phone

# Function to extract skills based on predefined list
def extract_skills(text):
    skills = []
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            skills.append(skill)
    return skills

# Function to extract education details based on predefined list
def extract_education(text):
    education_details = []
    for edu in EDUCATION_DB:
        if re.search(r'\b' + re.escape(edu) + r'\b', text, re.IGNORECASE):
            education_details.append(edu)
    return education_details

# Function to extract company names and experience
def extract_experience(text):
    # Simple keyword-based extraction for companies (e.g., look for 'Inc', 'LLC', 'Ltd', etc.)
    companies = re.findall(r'\b\w+(?:\s\w+)*(?: Inc| LLC| Ltd| Technologies)\b', text)
    return companies

# Main Streamlit app
def main():
    st.title("Smart Resume Analyzer (without SpaCy)")
    
    st.write("Upload your resume in PDF format and extract relevant details such as skills, education, experience, and contact information.")

    # File uploader
    pdf_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

    if pdf_file:
        # Extract text from the uploaded PDF
        resume_text = extract_text_from_pdf(pdf_file)
        
        # Display the raw text
        st.subheader("Extracted Resume Text:")
        st.write(resume_text)

        # Extract and display contact details
        email, phone = extract_contact_details(resume_text)
        st.subheader("Contact Information:")
        st.write(f"Email: {', '.join(email) if email else 'No email found'}")
        st.write(f"Phone: {', '.join(phone) if phone else 'No phone number found'}")

        # Extract and display skills
        skills = extract_skills(resume_text)
        st.subheader("Extracted Skills:")
        st.write(", ".join(skills) if skills else "No skills found")

        # Extract and display experience (companies)
        experience = extract_experience(resume_text)
        st.subheader("Work Experience (Companies):")
        st.write(", ".join(experience) if experience else "No experience found")

        # Extract and display education
        education = extract_education(resume_text)
        st.subheader("Education Details:")
        st.write(", ".join(education) if education else "No education details found")

if __name__ == "__main__":
    main()
