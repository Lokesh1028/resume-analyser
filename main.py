import streamlit as st
import PyPDF2
import io
import os
from groq import Groq

# Set up Groq client
client = Groq(api_key="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")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_resume(resume_text, job_description):
    prompt = f"""
    Analyze the following resume against the job description:
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    Please provide:
    1. ATS compatibility score (0-100)
    2. Key strengths matching the job requirements
    3. Areas where the candidate's profile falls short
    4. Specific suggestions to improve the resume
    5. What needs to be changed to make the candidate ideal for this position
    """
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="deepseek-r1-distill-llama-70b",
        max_tokens=1000,
        temperature=0.7
    )
    
    return response.choices[0].message.content

def main():
    st.title("Resume Analyzer")
    st.write("Upload your resume and enter a job description to get personalized feedback")
    
    # File uploader for resume
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
    
    # Text area for job description
    job_description = st.text_area("Enter the job description", height=200)
    
    if st.button("Analyze"):
        if uploaded_file is not None and job_description:
            with st.spinner("Analyzing your resume..."):
                # Extract text from PDF
                resume_text = extract_text_from_pdf(uploaded_file)
                
                # Analyze resume against job description
                analysis = analyze_resume(resume_text, job_description)
                
                # Display results
                st.subheader("Analysis Results")
                st.markdown(analysis)
        else:
            st.error("Please upload a resume and enter a job description")

if __name__ == "__main__":
    main()