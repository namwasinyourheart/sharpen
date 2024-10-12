import streamlit as st

st.set_page_config(layout="wide")
st.title("App for IELTS Paraphrase Scoring")


col1, col2 = st.columns(2)
with col1:
    st.subheader("Original Text")
    orig_text = """
Tesla has unveiled the Cybercab, a new electric vehicle dedicated to self-driving that lacks a steering wheel or pedals.

Priced at under $30,000, this vehicle is designed without a steering wheel or pedals and features two distinctive gull-wing doors

The operating cost is projected to be approximately 20 cents per mile, making it a cost-effective option for users

It supports “inductive charging,” eliminating the need for traditional plug-in methods

Tesla owners will have the opportunity to list their vehicles as robotaxis, providing an innovative way to generate income.
"""
    st.write(orig_text)

with col2:
    st.subheader("Enter your paraphrase")
    paraphrased_text = st.text_area("Let's paraphrase it", height=200)

    # Tesla has unveiled the Cybercab, a new electric vehicle dedicated to self-driving that lacks a steering wheel or pedals.

    # Priced at under $30,000, this vehicle is designed without a steering wheel or pedals and features two distinctive gull-wing doors

    # The operating cost is projected to be approximately 20 cents per mile, making it a cost-effective option for users

    # It supports “inductive charging,” eliminating the need for traditional plug-in methods

    # Tesla owners will have the opportunity to list their vehicles as robotaxis, providing an innovative way to generate income.


# Review section
review = """
**Task Reponse**  
**Lexical Resource**  
**Coherence & Cohesion**  
**Gramamtical Range & Accuracy**  
"""
st.write(review)