import streamlit as st
import spacy
import re
from PyPDF2 import PdfReader

# Load SpaCy's NLP model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Function to extract email and phone number using regex
def extract_contact_info(resume_text):
    phone = re.findall(r'\b\d{10}\b', resume_text)
    email = re.findall(r'\S+@\S+', resume_text)
    return email, phone

# Function to analyze resume content using SpaCy NLP
def analyze_resume(resume_text):
    doc = nlp(resume_text)

    # Extract different entities
    skills = []
    experience = []
    education = []

    for ent in doc.ents:
        if ent.label_ == 'ORG':  # Organizations for work experience
            experience.append(ent.text)
        elif ent.label_ == 'DATE':  # Dates for education/work periods
            education.append(ent.text)
        elif ent.label_ == 'PERSON':  # Use person names as proxy for skills
            skills.append(ent.text)

    # Deduplicate the lists
    skills = list(set(skills))
    experience = list(set(experience))
    education = list(set(education))

    return skills, experience, education

# Main function to create the Streamlit web app
def main():
    st.title("Smart Resume Analyzer")
    st.write("Upload your resume in PDF format to analyze skills, work experience, and education details.")

    # File uploader for the resume
    pdf_file = st.file_uploader("Upload Resume", type=["pdf"])

    if pdf_file is not None:
        # Extract text from the uploaded PDF
        resume_text = extract_text_from_pdf(pdf_file)

        # Display the extracted text (full resume content)
        st.subheader("Full Resume Text:")
        st.write(resume_text)

        # Extract contact information
        email, phone = extract_contact_info(resume_text)
        st.subheader("Contact Information:")
        st.write(f"Email: {', '.join(email) if email else 'Not found'}")
        st.write(f"Phone: {', '.join(phone) if phone else 'Not found'}")

        # Analyze the resume text with NLP
        skills, experience, education = analyze_resume(resume_text)

        # Display extracted skills
        st.subheader("Extracted Skills:")
        if skills:
            st.write(", ".join(skills))
        else:
            st.write("No skills detected.")

        # Display extracted experience
        st.subheader("Extracted Work Experience (Organizations):")
        if experience:
            st.write(", ".join(experience))
        else:
            st.write("No work experience detected.")

        # Display extracted education details
        st.subheader("Extracted Education:")
        if education:
            st.write(", ".join(education))
        else:
            st.write("No education details detected.")

if __name__ == "__main__":
    main()
