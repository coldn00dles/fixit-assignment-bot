import streamlit as st
import requests

backend_url = "http://0.0.0.0:7860"
st.header('fiXit Assignment', divider='orange')
st.header('Document-based QA Chatbot')

if 'uploadFlag' not in st.session_state:
    upload = st.file_uploader("Upload a DOCX file", type="docx")
    if upload:
        files = {'file': upload.getvalue()}
        response = requests.post(f"{backend_url}/uploaddoc", files=files)
        if response.status_code == 200:
            st.success("Document uploaded sucessfully")
            st.session_state.uploadFlag = True

if 'uploadFlag' in st.session_state:
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    question = st.text_input("Enter your question/query: ")
    if question:
        response = requests.post(f"{backend_url}/question", json={"question": question})
        if response.status_code == 200:
            answer = response.json().get("answer")
            st.session_state.chat_history.append(("user", question))
            st.session_state.chat_history.append(("assistant", answer))
        else:
            st.error("Failed to get an answer from the backend.")
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)