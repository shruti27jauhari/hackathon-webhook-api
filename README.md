# HackRX RAG System - Insurance Document Q&A

## 🎯 Hackathon Compliance

This project implements a **LLM-Powered Intelligent Query–Retrieval System** that meets all hackathon requirements:

### ✅ **Fully Compliant Features**
- **Document Processing**: PDF, DOCX, and email support
- **Semantic Search**: ChromaDB vector database with embeddings
- **LLM Integration**: Local TinyLlama model via Ollama
- **Structured Output**: JSON responses with explainable decisions
- **API Endpoints**: FastAPI backend with authentication
- **Batch Processing**: Multiple questions in single request
- **Blob URL Support**: Remote document processing

## 🚀 **Quick Start**

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install and Setup Ollama
```bash
# Download Ollama from https://ollama.com/download
# Pull TinyLlama model (optimized for memory)
ollama pull tinyllama
```

### 3. Run the API Server
```bash
python api.py
```

### 4. Test the API
```bash
python test_api.py
```

## 📡 **API Endpoints**

### Base URL: `http://localhost:8000/api/v1`

#### POST `/hackrx/run`
**Authentication**: `Bearer 6c10ec95ab42554f16af3233d5bea54461de3241715aba4e44148e8be9ea5ea8`

**Request Body**:
```json
{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=...",
    "questions": [
        "What is the grace period for premium payment?",
        "Does this policy cover maternity expenses?"
    ]
}
```

**Response**:
```json
{
    "answers": [
        "A grace period of thirty days is provided...",
        "Yes, the policy covers maternity expenses..."
    ]
}
```

#### GET `/health`
Health check endpoint

## 🏗️ **System Architecture**

1. **Input Documents** → Blob URL processing
2. **LLM Parser** → Query structure extraction
3. **Embedding Search** → ChromaDB semantic retrieval
4. **Clause Matching** → Top-k similarity matching
5. **Logic Evaluation** → TinyLlama decision processing
6. **JSON Output** → Structured response with explanations

## 🎮 **Alternative: Streamlit UI**

For local testing and development:
```bash
streamlit run app.py
```

## 📊 **Evaluation Criteria Compliance**

- ✅ **Accuracy**: Precise query understanding and clause matching
- ✅ **Token Efficiency**: Optimized TinyLlama usage
- ✅ **Latency**: Fast response with local processing
- ✅ **Reusability**: Modular code architecture
- ✅ **Explainability**: Clear decision reasoning with clause references

## 🔧 **Technical Stack**

- **Backend**: FastAPI
- **Vector DB**: ChromaDB (local alternative to Pinecone)
- **LLM**: TinyLlama (local alternative to GPT-4)
- **Embeddings**: Sentence Transformers
- **Document Processing**: pdfplumber, python-docx, email

## 📝 **Notes**

- All processing is local (no data leaves your machine)
- Optimized for memory constraints (uses TinyLlama)
- Supports both API and web interface
- Ready for hackathon submission 