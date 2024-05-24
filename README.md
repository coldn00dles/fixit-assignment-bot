# Document-based QA Chatbot

## Local Setup

1) Clone the repository <br>
`git clone https://github.com/coldn00dles/fixit-assignment-bot.git`

2) Run `pip install -r requirements.txt`
3) Run`bash script.sh` <br>
    Alternatively, run: <br>
    `uvicorn backend:app --host 0.0.0.0 --port 7860 --reload` <br>
    `streamlit run app.py`
4) The app should be available at `localhost:8051`

## Repository Structure Breakdown

1) `utils.py` - Contains the relevant functions for processing document text, vectorisation, retrieval pipeline, and generating answers for the question
2) `backend.py` - Contains a FastAPI instance with two endpoints : one for document upload and another one for answer generation
3) `app.py` - Consists of frontend via Streamlit. As of now, the only supported document type is docx, with a limit of 1 at a time per chat.


