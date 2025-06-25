'''import streamlit as st
from PIL import Image
import base64
import PyPDF2

# Page configuration
st.set_page_config(page_title="UK IT - Job Predictor", page_icon="💼", layout="wide")
st.set_page_config(page_title="Prediction", page_icon="🔍")


# Set background image
def add_bg(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/webp;base64,{encoded_string.decode()}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}

        .transparent-box {{
            background-color: black;
            width: 100%;
            padding: 1rem 0;
            margin: 0;
            position: fixed;
            top: 0;
            left: 0;
            text-align: center;
            z-index: 999;
        }}

        .job-title {{
            font-size: 4rem;
            font-weight: bold;
            color: #D2E8BA;
            margin: 0;
        }}

        .main-content {{
            margin-top: 7rem;  /* Push content below the fixed header */
            padding-left: 3rem;
            padding-right: 3rem;
        }}

        .content-box {{
            background-color: rgba(175, 205, 184, 0.7);
            color: black;
            max-width: 10900px;
            z-index: 999;
            padding: 2rem 3rem;
            border-radius: 5px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            font-size: 16px;
            line-height: 2;
            text-align: left;
            margin-bottom: 2rem;
        }}

        .upload-header {{
            color:#D2E8BA !important;
            font-size: 2rem !important;
            font-weight: bold !important;
        }}

        .upload-subtext {{
            color: #D2E8BA!important;
            font-size: 1rem !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg('imgg.webp')

# Add sidebar navigation
with st.sidebar:
    st.markdown("After uploading your resume, click on the **Prediction** page in the sidebar to see results.")
    st.markdown("---")

# Transparent full-width header
st.markdown('<div class="transparent-box"><div class="job-title">JOB PREDICTOR</div></div>', unsafe_allow_html=True)

# Main content left-aligned and pushed down
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Combined Welcome + Why Use This App Section
st.markdown("""
<div class="content-box">
    <h2>Welcome!</h2>
    <p>This smart application uses <strong>Natural Language Processing (NLP)</strong> and <strong>Machine Learning (ML)</strong> to analyze your resume and recommend the most suitable job roles.</p>
    <h4 style="color:black;">Why use this app?</h4>
    <p>This app simplifies and speeds up the job search and recruitment process by using advanced natural language processing techniques to understand both candidate profiles and job requirements deeply. It reduces the time recruiters spend sifting through countless applications and helps job seekers find roles that truly match their skills and career goals. By minimizing human bias and offering personalized, data-driven recommendations, this app increases the chances of successful hires and satisfying careers. Whether you’re a recruiter looking for the right talent or a job seeker aiming for the perfect fit, this app makes the entire experience smarter, fairer, and more efficient.</p>
</div>
""", unsafe_allow_html=True)

# File Upload Section with black text
st.markdown('<div class="upload-header">Upload Your Resume</div>', unsafe_allow_html=True)
st.markdown('<div class="upload-subtext">Upload your resume (PDF or TXT only)</div>', unsafe_allow_html=True)

uploaded_resume = st.file_uploader("", type=["txt", "pdf"])

if uploaded_resume is not None:
    resume_text = ""

    if uploaded_resume.name.endswith('.pdf'):
        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(uploaded_resume)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text
    else:
        # Extract text from TXT file
        resume_text = uploaded_resume.read().decode('utf-8')

    # Save extracted text to a file
    with open("uploaded_resume.txt", "w", encoding='utf-8') as f:
        f.write(resume_text)

    st.success("Resume uploaded successfully! 🎉")
    st.write("Go to the **Prediction** page from the sidebar to see your results.")

st.markdown('</div>', unsafe_allow_html=True)
'''