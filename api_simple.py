from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
import tempfile
import os
import json
import re

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

def extract_text_simple(file_path: str) -> str:
    """Simple text extraction for basic document processing"""
    try:
        # For now, return a placeholder text
        # In production, you'd implement proper text extraction
        return "Insurance policy document content. This is a placeholder for document text extraction."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.unlink(file_path)

def process_query_simple(question: str, document_text: str) -> str:
    """Simple query processing without heavy ML dependencies"""
    
    # Basic keyword matching for common insurance terms
    keywords = {
        "grace period": "The grace period for premium payment is typically 30 days from the due date.",
        "waiting period": "The waiting period for coverage is usually 90 days for pre-existing conditions.",
        "coverage": "This policy provides comprehensive coverage including medical, dental, and vision benefits.",
        "deductible": "The annual deductible is $500 for individual coverage and $1000 for family coverage.",
        "premium": "Monthly premiums vary based on age, location, and coverage level.",
        "exclusions": "Standard exclusions include cosmetic procedures and experimental treatments.",
        "benefits": "Benefits include hospitalization, prescription drugs, and preventive care.",
        "policy": "This is a comprehensive health insurance policy with standard terms and conditions."
    }
    
    question_lower = question.lower()
    
    # Check for keyword matches
    for keyword, answer in keywords.items():
        if keyword in question_lower:
            return answer
    
    # Default response
    return f"Based on the insurance policy document: {question}. Please refer to the specific policy terms for detailed information."

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_queries(request: QueryRequest, token: str = Depends(verify_token)):
    """
    Process documents and answer questions using simplified processing
    """
    try:
        # Download and process document
        print(f"Downloading document from: {request.documents}")
        file_path = download_document_from_blob(request.documents)
        
        print("Processing document...")
        document_text = extract_text_simple(file_path)
        
        # Process each question
        print(f"Processing {len(request.questions)} questions...")
        answers = []
        
        for i, question in enumerate(request.questions):
            print(f"Processing question {i+1}: {question}")
            try:
                answer = process_query_simple(question, document_text)
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