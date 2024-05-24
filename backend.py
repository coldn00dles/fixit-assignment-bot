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
    """
    Endpoint for handling document upload. \n
    
    Args : 
    file (File) : The file received from frontend
    
    Returns : 
    res (dict) : A JSON with appropiate upload status
    """
    content = await file.read()
    file = BytesIO(content)
    
    text, tables = textprocessing(file)

    text_embds = embed_query(text)
    table_texts = ["-".join(["|".join(row) for row in table]) for table in tables]   #adding denotions for llm to bifurcate between text and table
    table_embds = embed_query(table_texts)

    vectordb = setvecdb(text_embds, table_embds, text, table_texts)
    document_data["vectordb"] = vectordb
    res = {"message": "Document uploaded and processed successfully"}
    return res

@app.post("/question")
async def processquestion(question: Q):
    """
    Endpoint for processing question generation of answer. \n
    
    Args : 
    question (Q) : Question asked by user
    
    Returns : 
    ans (dict) : JSON with appropiate answer for user's question
    """
    query_text = question.question
    vectordb = document_data.get("vectordb")
    if vectordb is None:
        return {"error": "No document uploaded"}
    
    search_results = retriever(vectordb, query_text)
    context = "\n".join(search_results['content'].sum())
    answer = generate_answer(query_text, context)
    ans = {"answer": answer}
    return ans