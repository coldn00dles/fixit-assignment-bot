from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from utils import *
from io import BytesIO

document_data = {}

app = FastAPI()
class Q(BaseModel):
    question: str

from utils import *


@app.post("/uploaddoc")
async def upload_document(file: UploadFile = File()):
    content = await file.read()
    file = BytesIO(content)
    
    text, tables = textprocessing(file)

    text_embds = embed_query(text)
    table_texts = ["-".join(["|".join(row) for row in table]) for table in tables]
    table_embds = embed_query(table_texts)

    vectordb = setvecdb(text_embds, table_embds, text, table_texts)
    document_data["vectordb"] = vectordb
    return {"message": "Document uploaded and processed successfully"}

@app.post("/question")
async def processquestion(question: Q):
    query_text = question.question
    vectordb = document_data.get("vectordb")
    if vectordb is None:
        return {"error": "No document uploaded"}
    
    search_results = retriever(vectordb, query_text)
    context = "\n".join(search_results['content'].sum())
    answer = generate_answer(query_text, context)
    return {"answer": answer}