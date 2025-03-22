import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/assess"

st.set_page_config(layout="wide")
st.title("App for IELTS Paraphrase Scoring")


col1, col2 = st.columns(2)
with col1:
    st.subheader("Original Text")
#     orig_text = """
# Tesla has unveiled the Cybercab, a new electric vehicle dedicated to self-driving that lacks a steering wheel or pedals.

# Priced at under $30,000, this vehicle is designed without a steering wheel or pedals and features two distinctive gull-wing doors

# The operating cost is projected to be approximately 20 cents per mile, making it a cost-effective option for users

# It supports “inductive charging,” eliminating the need for traditional plug-in methods

# Tesla owners will have the opportunity to list their vehicles as robotaxis, providing an innovative way to generate income.
# """
    orig_text = st.text_area("Enter original text:", height=200)
    st.write(orig_text)

with col2:
    st.subheader("Your paraphrase")
    your_paraphrase = st.text_area("Let's paraphrase it", height=200)
    st.write(your_paraphrase)

    # Tesla has unveiled the Cybercab, a new electric vehicle dedicated to self-driving that lacks a steering wheel or pedals.

    # Priced at under $30,000, this vehicle is designed without a steering wheel or pedals and features two distinctive gull-wing doors

    # The operating cost is projected to be approximately 20 cents per mile, making it a cost-effective option for users

    # It supports “inductive charging,” eliminating the need for traditional plug-in methods

    # Tesla owners will have the opportunity to list their vehicles as robotaxis, providing an innovative way to generate income.
input = {
    "original_text": orig_text,
    "your_paraphrase":your_paraphrase
}

from server import WritingAssessment
response = requests.post(f"{BACKEND_URL}", json=input)
assessment = WritingAssessment(**response.json())

# Review section

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Task Response")
    st.write("Score:", assessment.task_response.score)
    # st.write("Concerns:", assessment.task_response.concerns)
    for concern in assessment.task_response.concerns:
        st.write(f"- {concern}")

    

with col2: 
    st.subheader("Lexical Resource")
    st.write("Score:", assessment.vocabulary.score)
    # st.write("Concerns:", assessment.task_response.concerns)
    for concern in assessment.vocabulary.concerns:
        st.write(f"- {concern}")


with col3:
    st.subheader("Coherence & Cohesion")
    st.write("Score:", assessment.cohesion_and_coherence.score)
    # st.write("Concerns:", assessment.task_response.concerns)
    for concern in assessment.cohesion_and_coherence.concerns:
        st.write(f"- {concern}")


with col4: 
    st.subheader("Grammar Range & Accuracy")
    st.write("Score:", assessment.grammar.score)
    # st.write("Concerns:", assessment.task_response.concerns)
    for concern in assessment.grammar.concerns:
        st.write(f"- {concern}")

st.subheader("Reference Answers")
for answer in assessment.reference_answers:
    st.write(f"- {answer}")

st.subheader("Overall")
# st.write(assessment)
st.write("Score:", assessment.overall.score)
# st.write("Concerns:", assessment.task_response.concerns)
st.write(assessment.overall.main_issue)



# review = """
# **Task Reponse**  
# **Lexical Resource**  
# **Coherence & Cohesion**  
# **Gramamtical Range & Accuracy**  
# """
# st.write(review)