import streamlit as st
import requests

API_URL = "http://localhost:8000/analyze"

st.set_page_config(page_title="SmellSense AI")

st.title("SmellSense AI")
st.subheader("Automated Code Smell Detection Chatbot")

uploaded_file = st.file_uploader("Upload Java File", type=["java"])

if uploaded_file:

    st.write("Analyzing code...")

    response = requests.post(
        API_URL,
        files={"file": uploaded_file}
    )

    if response.status_code == 200:

        data = response.json()

        st.write("### Static Detection")
        st.write(data["static_engine"])

        st.write("### Metric Detection")
        st.write(data["metric_engine"])

        st.write("### LLM Semantic Detection")
        st.write(data["llm_engine"])

    else:

        st.write("Error analyzing file.")