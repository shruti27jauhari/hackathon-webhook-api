from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
import tempfile
import os
from document_loader import extract_text_from_pdf, extract_text_from_docx, extract_text_from_eml
from rag_engine import RAGEngine
import json

app = FastAPI(title="Insurance Policy Analyzer API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication
TEAM_TOKEN = "6c10ec95ab42554f16af3233d5bea54461de3241715aba4e44148e8be9ea5ea8"

def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    if token != TEAM_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return token

# Pydantic models
class QueryRequest(BaseModel):
    documents: str  # Blob URL
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

# Global RAG engine instance
rag_engine = RAGEngine()

def download_document_from_blob(blob_url: str) -> str:
    """Download document from blob URL and return file path"""
    try:
        response = requests.get(blob_url)
        response.raise_for_status()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name
        
        return temp_file_path
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to download document: {str(e)}")

def process_document(file_path: str) -> str:
    """Process document and extract text"""
    try:
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as f:
                return extract_text_from_pdf(f)
        elif file_path.endswith('.docx'):
            with open(file_path, 'rb') as f:
                return extract_text_from_docx(f)
        elif file_path.endswith('.eml'):
            with open(file_path, 'rb') as f:
                return extract_text_from_eml(f)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.unlink(file_path)

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_queries(request: QueryRequest, token: str = Depends(verify_token)):
    """
    Process documents and answer questions using RAG system
    """
    try:
        # Download and process document
        print(f"Downloading document from: {request.documents}")
        file_path = download_document_from_blob(request.documents)
        
        print("Processing document...")
        document_text = process_document(file_path)
        
        # Add document to RAG engine
        print("Adding document to RAG engine...")
        rag_engine.add_document(document_text, {'source': 'blob_url'})
        
        # Process each question
        print(f"Processing {len(request.questions)} questions...")
        answers = []
        
        for i, question in enumerate(request.questions):
            print(f"Processing question {i+1}: {question}")
            try:
                response = rag_engine.process_query(question)
                
                # Extract the answer or create a meaningful response
                if 'answer' in response and response['answer']:
                    answer = response['answer']
                elif 'summary' in response and response['summary']:
                    answer = response['summary']
                else:
                    answer = f"Based on the policy document: Unable to provide a specific answer to this question."
                
                answers.append(answer)
                
            except Exception as e:
                print(f"Error processing question {i+1}: {str(e)}")
                answers.append(f"Error processing question: {str(e)}")
        
        return QueryResponse(answers=answers)
        
    except Exception as e:
        print(f"Error in run_queries: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Insurance Policy Analyzer API is running"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Insurance Policy Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/v1/health",
            "run_queries": "/api/v1/hackrx/run"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 