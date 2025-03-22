# client.py
import streamlit as st
import requests
from server import WritingAssessment

BACKEND_URL = "http://127.0.0.1:8000/assess"

st.set_page_config(layout="wide")
st.title("App for IELTS Paraphrase Scoring")

def get_text_input(label):
    return st.text_area(label, height=200)

def display_score(category, score, concerns):
    st.subheader(category)
    st.write("Score:", score)
    for concern in concerns:
        st.write(f"- {concern}")

def fetch_assessment(input_data):
    try:
        response = requests.post(BACKEND_URL, json=input_data)
        response.raise_for_status()
        return WritingAssessment(**response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching assessment: {e}")
        return None

col1, col2 = st.columns(2)
with col1:
    st.subheader("Original Text")
    orig_text = get_text_input("Enter original text:")
with col2:
    st.subheader("Your Paraphrase")
    your_paraphrase = get_text_input("Let's paraphrase it")

if st.button("Assess Paraphrase"):
    assessment = fetch_assessment({"original_text": orig_text, "your_paraphrase": your_paraphrase})
    if assessment:
        col1, col2, col3, col4 = st.columns(4)
        with col1: display_score("Task Response", assessment.task_response.score, assessment.task_response.concerns)
        with col2: display_score("Lexical Resource", assessment.vocabulary.score, assessment.vocabulary.concerns)
        with col3: display_score("Coherence & Cohesion", assessment.cohesion_and_coherence.score, assessment.cohesion_and_coherence.concerns)
        with col4: display_score("Grammar Range & Accuracy", assessment.grammar.score, assessment.grammar.concerns)
        
        st.subheader("Reference Answers")
        for answer in assessment.reference_answers:
            st.write(f"- {answer}")
        
        st.subheader("Overall Score")
        st.write("Score:", assessment.overall.score)
        st.write(assessment.overall.main_issue)