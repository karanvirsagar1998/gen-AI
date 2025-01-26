# To extract text from a resume using Python,
# we will use libraries like PyPDF2 or pdfplumber for PDFs, and docx

# pip install pdfplumber
import pdfplumber

def extract_resume(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text=''
        for page in pdf.pages:
            text+=page.extract_text()
        return text

pdf_path = "resumes/resume.pdf"
resume_text = extract_resume(pdf_path)
print(resume_text) #simplest way to parse text from a resume