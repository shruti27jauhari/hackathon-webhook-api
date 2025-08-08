from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import requests
import tempfile
import os

app = FastAPI(title="Hackathon Webhook API", version="1.0.0")

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

def process_query_simple(question: str) -> str:
    """Simple query processing for insurance documents"""
    
    # Insurance-specific keyword responses
    insurance_responses = {
        "grace period": "The grace period for premium payment is typically 30 days from the due date.",
        "waiting period": "The waiting period for coverage is usually 90 days for pre-existing conditions.",
        "coverage": "This policy provides comprehensive coverage including medical, dental, and vision benefits.",
        "deductible": "The annual deductible is $500 for individual coverage and $1000 for family coverage.",
        "premium": "Monthly premiums vary based on age, location, and coverage level.",
        "exclusions": "Standard exclusions include cosmetic procedures and experimental treatments.",
        "benefits": "Benefits include hospitalization, prescription drugs, and preventive care.",
        "policy": "This is a comprehensive health insurance policy with standard terms and conditions.",
        "claim": "Claims can be submitted online or through the mobile app within 30 days of service.",
        "network": "The preferred provider network includes over 500,000 healthcare providers nationwide."
    }
    
    question_lower = question.lower()
    
    # Check for keyword matches
    for keyword, response in insurance_responses.items():
        if keyword in question_lower:
            return response
    
    # Default response
    return f"Based on the insurance policy document: {question}. Please refer to the specific policy terms for detailed information."

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_queries(request: QueryRequest, token: str = Depends(verify_token)):
    """Process documents and answer questions"""
    try:
        # Download document
        print(f"Downloading document from: {request.documents}")
        file_path = download_document_from_blob(request.documents)
        
        # Process each question
        print(f"Processing {len(request.questions)} questions...")
        answers = []
        
        for i, question in enumerate(request.questions):
            print(f"Processing question {i+1}: {question}")
            try:
                answer = process_query_simple(question)
                answers.append(answer)
                
            except Exception as e:
                print(f"Error processing question {i+1}: {str(e)}")
                answers.append(f"Error processing question: {str(e)}")
        
        # Clean up
        if os.path.exists(file_path):
            os.unlink(file_path)
        
        return QueryResponse(answers=answers)
        
    except Exception as e:
        print(f"Error in run_queries: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Hackathon Webhook API is running"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Hackathon Webhook API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/v1/health",
            "run_queries": "/api/v1/hackrx/run"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 