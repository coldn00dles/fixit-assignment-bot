import streamlit as st
import requests

backend_url = "http://localhost:7860"
st.header('fiXit Assignment', divider='orange')   #title and sub-title
st.header('Document-based QA Chatbot')

if 'uploadFlag' not in st.session_state:          #checking if document has been uploaded 
    upload = st.file_uploader("Upload your document (in DOCX)", type="docx")   #if not, upload id prompted
    if upload:
        files = {'file': upload.getvalue()}               #contents of the document are sent as bytes
        response = requests.post(f"{backend_url}/uploaddoc", files=files)
        if response.status_code == 200:                   #once upload has been finalised and processed by the backend endpoint, the upload flag is set to true
            st.success("Document uploaded sucessfully")
            st.session_state.uploadFlag = True                  

if 'uploadFlag' in st.session_state:                    #enable chat once upload flag is set to true
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    question = st.text_input("Enter your question/query: ")
    if question:                                                    #question is parametrised and sent to answer endpoint of backend
        response = requests.post(f"{backend_url}/question", json={"question": question})
        if response.status_code == 200:
            answer = response.json().get("answer")                  #llm generates answer and returns it back
            st.session_state.chat_history.append(("user", question))
            st.session_state.chat_history.append(("assistant", answer))
        else:
            st.error("Failed to get an answer from the backend.")
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)                                     #answer and question is displayed 