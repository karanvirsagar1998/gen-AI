import spacy
# Imports the SpaCy library, which is a powerful and efficient tool for (NLP).
#Why We Use It: To extract structured information from resumes such as names, emails, phone numbers, skills, and experiences.

import re
#Imports Python’s built-in regular expression module. To search, match, and manipulate text using patterns.

from docx import Document
# Imports the Document class from the python-docx library. To read, edit, and write Microsoft Word documents (.docx files).

import PyPDF2
#Imports the PyPDF2 library, which is used to work with PDF files.Imports the PyPDF2 library, which is used to work with PDF files.
# We did not use pdfplumber library here because pdfplumber specializes in precise text extraction and
# is particularly suited for handling PDFs with complex layouts, such as
# tables, multi-column formats, or text embedded within graphical elements. 

nlp = spacy.load("en_core_web_sm")

def get_text_from_pdf_resume(pdf_path):
    with open(pdf_path, 'rb') as pdf: #Opens the specified pdf_file in binary read mode ('rb').
        reader = PyPDF2.PdfReader(pdf) #Creates an instance of the PdfReader class from the PyPDF2 library, passing the opened file as an argument.
        text=""
        for page in reader.pages:
            text+=page.extract_text()
        return text

def get_text_from_word_resume(word_path):
    doc = Document(word_path) #Document class from the python-docx library to load the .docx file.
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text) #Joins all the text from the full_text list into a single string, with each paragraph separated by a newline (\n).
    
def extact_email(doc):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, doc)
    return emails if emails else None

def extract_skills(doc):
    skills = ["maintenance", "coordination", "supervision","reporting","management", "Fire alarm handling", "after-hours support"]
    found_skills = [skill for skill in skills if skill.lower() in doc.lower()]
    return found_skills

def extract_we(doc):
    we = []
    experience_pattern = r"(?:[A-Za-z]+(?: [A-Za-z]+)*)\s*(\d{4}[-/]\d{4}|\d{4})" 
    experience = re.findall(experience_pattern, doc)
    for exp in experience:
        we.append(exp)
    return we

def analyze_resume(resume_text):
    doc = nlp(resume_text) # Process the text using SpaCy
    # named_entities = [(ent.text, ent.label_) for ent in doc.ents]
    # email = extact_email(resume_text)
    skills = extract_skills(resume_text)
    # we = extract_we(resume_text)
    # return{
    #     "Named Entities": named_entities,
    #     "Skills": skills,
    #     "Work Experience": we,
    #     "Email" : email            
    # }
    return skills

resume_text = get_text_from_pdf_resume("resumes/document.pdf") #get text from resume

def text_prepprocess(resume_text): #ensures that both the resume and job description are cleaned, standardized, and ready for comparison.
    text = resume_text.lower() #Convert text to lowercase
    text = re.sub(r'[^a-z\s]', '', text) #Remove special characters, numbers, and punctuation
    # r'[^a-z\s]': Matches anything that isn’t a lowercase letter or space.
    # re.sub(): Replaces matched characters with an empty string ('').
    #Tokenize and lemmatize using SpaCy
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    return " ".join(tokens) #Join the processed tokens back into a single string

# resume_analysis = analyze_resume(resume_text)

jd = get_text_from_pdf_resume("resumes/jd.pdf")
job_desc_processed = text_prepprocess(jd)
resume_processed = text_prepprocess(resume_text)

# Extract important keywords (like skills, tools, and roles) from both the resume and job description.
# Use set operations or NLP techniques to find overlapping keywords.
# Calculate a similarity score based on the match.

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# CountVectorizer: Converts text into a numerical format (word frequency vectors).
# cosine_similarity: Measures how similar two numerical vectors are.

def calculate_similarity(resume, job_description): # Accepts two preprocessed strings: the resume and job description.
    texts = [resume, job_description]  # Combines them into a list (texts), so both can be vectorized together.
    vectorizer = CountVectorizer()
    vectorized_texts = vectorizer.fit_transform(texts)
    similarity_matrix = cosine_similarity(vectorized_texts)
    similarity_score = similarity_matrix[0][1]
    return round(similarity_score * 100, 2)

def calculate_detailed_score(resume, job_description):
    resume_sections = {
        "skills":", ".join(analyze_resume(resume)),
    }
    job_description = {
        "skills": "Oversee all on-site construction,Fire Alarm, after-hours,  management"+
                    " including maintenance, coordinating, and supervision of subcontractors, vendors, and laborers."
    }

    scores = {}
    for category in resume_sections:
        scores[category] = calculate_similarity(resume_sections[category], job_description[category])
    return scores



#Testing....
scores = calculate_detailed_score(resume_processed, job_desc_processed)
for category, score in scores.items():
    print(f"{category.capitalize()} Match: {score}%")