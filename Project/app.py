import base64
import io
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import debugpy
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# You may also need to install poppler to get pdf into images:
#  sudo apt-get update
# sudo apt-get install -y poppler-utils


def get_gemini_response(input, pdf_content, prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input, pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # converting the pdf to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # convert to bytes
        image_byte_arr = io.BytesIO()
        first_page.save(image_byte_arr, format = 'JPEG')
        image_byte_arr = image_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type":"image/jpeg",
                "data":base64.b64encode(image_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File uploaded")

# writing your prompt template

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description: ", key="input")
uploaded_file=st.file_uploader("Upload your resume in PDF", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")

submit1 = st.button("Tell me about my resume")
submit2 = st.button("How can I improve it")
submit3= st.button("Percentage match")

input_prompt1="""
    You are an experienced HR professional with technical expertise in the fields of Data Science, Full Stack Development, Big Data Engineering, Data Science, Data Analytics, and Data Analyst roles. Your task is to evaluate the provided resume against the job description for the specified profile(s).
    Please perform the following tasks:
    1. Professional Evaluation of Profile Fit:
    2. Evaluate whether the candidate’s profile (experience, skills, and education) aligns with the job description for the specified role (Data Scientist, Full Stack Developer, Big Data Engineer, Data Analyst, etc.).
    3. ssess the overall suitability of the candidate for the role.
    4. Provide a professional evaluation on how well the candidate's background matches the role's key requirements.
    5. Strengths in the Resume:
        Highlight the candidate's strengths in relation to the job description, focusing on:
        Key technical skills (e.g., programming languages, frameworks, tools) relevant to the ro    le.
    6. Work experience and accomplishments that align with the specific responsibilities and goals outlined in the job description.
    7. Educational qualifications, certifications, and any other relevant credentials that make the candidate stand out.
    8. Weaknesses and Gaps:
        Identify any weaknesses or gaps in the candidate's profile when compared to the job description, including:
        Missing or underrepresented technical skills or tools required for the role.
        Lack of relevant work experience or incomplete job descriptions in their past roles.
        Any deficiencies in required education or certifications for the role.
        Areas where the candidate may need further development or improvement to be a better fit for the job.
    9. Suggestions for Improvement:
        Provide professional suggestions on how the candidate can improve their resume or profile to better align with the job description, such as:
    10. Recommended technical skills or certifications to add.
        Possible rewording of previous job roles to better highlight relevant experience.
        Any educational or professional development opportunities that may benefit the candidate.
    11. Overall Recommendation:
        Offer a final recommendation based on the review:
    12. Is the candidate a good fit for the role, or would they need further improvements to be considered for an interview?
        Provide any insights that could help in making a decision whether to proceed with this candidate or not..
"""

input_prompt2="""
    You are the Director of HR with 20 years of experience in the fields of Data Science, Full Stack Development, Big Data Engineering, Data Science, and Data Analytics.
    Your task is to review a candidate's resume and provide detailed suggestions on how to improve their skills and qualifications to better align with the given job description
    1. Skills Match: Compare the candidate's listed skills with the required skills in the job description and highlight any gaps or missing key skills that should be added.
    2. Experience Relevance: Analyze the candidate’s work experience and suggest how they can present their achievements or responsibilities in a way that better aligns with the job description.
    3. Technical Competency: Ensure that the technical skills (e.g., programming languages, frameworks, tools) mentioned in the resume are relevant to the job and up-to-date with industry standards.
    4. Certifications and Education: Suggest additional certifications or educational qualifications that could be beneficial based on the role’s requirements.
    5. Soft Skills: Provide insights into any soft skills that are important for the position but might be lacking in the resume. For example, communication, problem-solving, leadership, etc.
    6. Overall Structure: Advise on the overall structure of the resume, including formatting, length, and presentation. Ensure that the most important skills and experiences are highlighted effectively."""

input_prompt3="""
    You are an AI model with a deep understanding of Applicant Tracking Systems (ATS). Your task is to analyze the candidate's resume against the given job description and provide feedback on how well the resume aligns with ATS requirements and also provice the metrics that how much percent does it matches with the job description. Please follow the steps below:
    1. Keyword Matching: Identify and extract key words and phrases from the job description (e.g., skills, certifications, tools, technologies). Cross-check them against the candidate's resume. Highlight any missing keywords or phrases that are critical for the ATS to flag the resume for consideration.
    2. Formatting Review: Assess the format of the resume for ATS compatibility. Ensure that the resume follows best practices (e.g., use of standard headings like "Work Experience," "Skills," "Education") and avoids ATS pitfalls such as images, graphics, or unusual fonts that could cause the ATS to miss important details.
    3. Job Title and Role Alignment: Compare the candidate's previous job titles and job descriptions with the role and requirements in the job description. Suggest optimizations or rewording that would improve alignment with the ATS.
    4. Section Optimization: Ensure that the candidate's resume includes all the necessary sections (e.g., summary, skills, experience, education, certifications). Ensure each section is well-organized and ATS-friendly.
    5. Actionable Verbs and Skills: Ensure the resume uses actionable and industry-standard verbs and skills (e.g., "Developed," "Led," "Implemented," etc.). Suggest using stronger, more specific verbs that are likely to be flagged by the ATS.
    6. Skills and Tools Optimization: Review the listed technical skills and tools in the resume. Ensure they are explicitly mentioned (e.g., programming languages, frameworks, tools like Python, Java, AWS, Hadoop). Suggest adding missing but relevant skills based on the job description.
    7. Job Experience Formatting: Evaluate how the candidate’s experience is presented (e.g., bullet points, job responsibilities, accomplishments). Ensure key metrics (e.g., performance indicators) are included to increase ATS score.
    9. Education and Certifications: Cross-check the candidate’s educational background and certifications with those listed in the job description. Suggest additional relevant certifications or education that would make the resume more ATS-compliant.
    10. ATS-Optimization Recommendations: After reviewing the resume, provide a final report with detailed recommendations on how to improve the resume for better ATS performance. Suggest how the resume should be restructured or enhanced to increase the likelihood of passing through ATS filters.
    11. Please analyze the following resume and job description, providing an in-depth review based on ATS standards. Focus on keyword optimization, formatting, and overall ATS alignment to improve the chances of the resume getting selected.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload a PDF")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload a PDF")

elif submit3:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("Percentage Match:")
        st.write(response)
    else:
        st.write("Please upload a PDF")