'''import streamlit as st
import pickle
from utils import preprocess_text
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Job Prediction Results", page_icon="🔮", layout="centered")

# Load model and vectorizer
model = pickle.load(open('job_predictor.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

st.title("🔮 Job Prediction Results")

try:
    with open("uploaded_resume.txt", "r", encoding="utf-8") as file:
        resume_text = file.read()

    processed_text = preprocess_text(resume_text)
    vectorized_input = vectorizer.transform([processed_text])

    prediction = model.predict(vectorized_input)[0]
    probabilities = model.predict_proba(vectorized_input)[0]

    st.header(f"🎯 Predicted Job Role: {prediction}")

    # Show probability chart
    st.subheader("📊 Job Role Probabilities")
    job_roles = model.classes_
    fig, ax = plt.subplots()
    ax.barh(job_roles, probabilities, color='skyblue')
    ax.set_xlabel('Probability')
    ax.set_ylabel('Job Roles')
    ax.set_xlim(0, 1)
    st.pyplot(fig)

    # Show top 3 matches
    st.subheader("🏆 Top 3 Recommended Roles")
    top3_indices = np.argsort(probabilities)[::-1][:3]
    for idx in top3_indices:
        st.write(f"- {job_roles[idx]}: {probabilities[idx]*100:.2f}%")

except FileNotFoundError:
    st.error("⚠️ Please upload your resume from the Home page first.")
'''