import streamlit as st
import pickle
from utils import preprocess_text
import numpy as np
import matplotlib.pyplot as plt
import PyPDF2
import base64

# Page config
st.set_page_config(page_title="Job Predictor", layout="wide")

# Background image function
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
            margin-top: 7rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }}
        .content-box {{
            background-color: rgba(175, 205, 184, 0.7);
            color: black;
            max-width: 900px;
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

# Fixed header
st.markdown('<div class="transparent-box"><div class="job-title">JOB PREDICTOR</div></div>', unsafe_allow_html=True)

# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Load model and vectorizer
@st.cache_resource
def load_model():
    loaded_model = pickle.load(open('job_predictor.pkl', 'rb'))
    loaded_vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
    return loaded_model, loaded_vectorizer

model, vectorizer = load_model()

# Main content
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if st.session_state.page == "home":
    # Home Page Content
    st.markdown("""
    <div class="content-box">
        <h2>Welcome!</h2>
        <p>This smart application uses <strong>Natural Language Processing (NLP)</strong> and <strong>Machine Learning (ML)</strong> to analyze your resume and recommend the most suitable job roles.</p>
        <h4 style="color:black;">Why use this app?</h4>
        <p>This app simplifies and speeds up the job search and recruitment process by using advanced NLP techniques to understand both candidate profiles and job requirements deeply. It reduces recruiter workload, helps job seekers find roles matching their skills, and minimizes bias for better hiring outcomes.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="upload-header">Upload Your Resume</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-subtext">Upload your resume (PDF or TXT only)</div>', unsafe_allow_html=True)

    uploaded_resume = st.file_uploader("Upload your resume here", type=["txt", "pdf"], label_visibility="collapsed")


    if uploaded_resume is not None:
        resume_text = ""

        if uploaded_resume.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(uploaded_resume)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    resume_text += text
        else:
            resume_text = uploaded_resume.read().decode('utf-8')

        st.session_state['resume_text'] = resume_text
        st.success("Resume uploaded successfully!")

        # Show Proceed Button
        proceed = st.button("Proceed to Prediction")

        if proceed:
            st.session_state.page = "prediction"
            st.rerun()

elif st.session_state.page == "prediction":
    st.markdown("""
    <div class="content-box"style="padding: 0.5rem 1rem; background-color: rgba(175, 205, 184, 0.7); color: black; border-radius: 10px;">
        <h2 style="margin: 0; font-weight: 800;">JOB PREDICTION RESULTS</h2>
    </div>
    """, unsafe_allow_html=True)

    resume_text = st.session_state.get('resume_text', None)

    if resume_text:
    # Resume Preview in Transparent Box with Black Text
        st.markdown(f"""
        <div class="content-box" style="color: black; padding: 0.5rem 1rem; background-color:rgba(175, 205, 184, 0.7);">
            <h4><b>Resume Preview</b></h4>
            <pre style="white-space: pre-wrap; font-size: 14px; color: black;">{resume_text[:1000]}</pre>
        </div>
        """, unsafe_allow_html=True)

        processed_text = preprocess_text(resume_text)
        vectorized_input = vectorizer.transform([processed_text])

        prediction = model.predict(vectorized_input)[0]
        probabilities = model.predict_proba(vectorized_input)[0]

        st.markdown(f"""
        <div style="color:black;">
            <h1>Predicted Job Role: {prediction}</h1>
        </div>
        """, unsafe_allow_html=True)


        # Probability chart
        # Probability chart with custom styling
        st.markdown(f"""
        <h3 style="color:black;">Job Role Probabilities</h3>
        """, unsafe_allow_html=True)

        job_roles = model.classes_
        fig, ax = plt.subplots(figsize=(8, 5))

        # Set black background
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')

        # Plot green bars
        ax.barh(job_roles, probabilities, color="#C6E0A9")

        # Set white labels and white axes
        ax.set_xlabel('Probability', color="#E7FFCE")
        ax.set_ylabel('Job Roles', color="#E7FFCE")
        ax.tick_params(axis='x', colors="#E7FFCE")
        ax.tick_params(axis='y', colors="#E7FFCE")

        # Set white axis lines
        for spine in ax.spines.values():
            spine.set_color('white')

        # Set x-axis limit
        ax.set_xlim(0, 1)

        st.pyplot(fig)

        # Top 3 recommendations
        top3_indices = np.argsort(probabilities)[::-1][:3]

        # Build the entire HTML block at once
        html_block = """
        <div class="content-box" style="font-size:1rem;background-color:rgba(175, 205, 184, 0.7); color: black; padding: 0.5rem 1rem; border-radius: 10px;">
            <h2 style="margin: 0; font-weight: 800;">Top 3 Recommended Roles</h2>
        """

        # Add predictions to the HTML block
        for idx in top3_indices:
            html_block += f"<p style='margin: 5px 0; font-weight:800;'>- {job_roles[idx]}: {probabilities[idx]*100:.2f}%</p>"

        # Close the HTML block
        html_block += "</div>"

        # Render the whole block at once
        st.markdown(html_block, unsafe_allow_html=True)



    else:
        st.warning("No resume found. Please upload your resume on the Home page.")

    if st.button("Go back to Home"):
        st.session_state.page = "home"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
