# Job Predictor

This is a Streamlit-based NLP-powered Resume Screening and Job Prediction App that analyzes resumes and predicts the most suitable IT job roles using machine learning.

---

## Features
-  Resume upload and text extraction (PDF or TXT files)
-  Natural Language Processing (NLP) based text preprocessing
-  Job role prediction using a trained ML model
-  Probability visualization with customized graphs
-  Top 3 recommended job roles display
-  Beautiful background and customized UI

---

## Project Structure
```text
resume_screener_job_predictor/
│
├── app.py                 # Main Streamlit app
├── utils.py               # Text preprocessing functions
├── job_predictor.pkl      # Trained job prediction model
├── vectorizer.pkl         # Vectorizer used for NLP processing
├── imgg.webp              # Background image
├── requirements.txt       # Required Python packages
└── README.md              # Project documentation
