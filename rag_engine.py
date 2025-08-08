import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from ollama_utils import call_ollama
import json
import re

class RAGEngine:
    def __init__(self, persist_directory='rag_db'):
        self.chroma_client = chromadb.Client(Settings(persist_directory=persist_directory))
        self.collection = self.chroma_client.get_or_create_collection('documents')
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def add_document(self, text, metadata):
        # Improved text chunking - split by sentences and paragraphs
        import nltk
        try:
            # Download punkt if not available
            nltk.download('punkt', quiet=True)
        except Exception:
            pass
        
        # Split into sentences first, then into chunks
        try:
            sentences = nltk.sent_tokenize(text)
        except Exception:
            # Fallback to simple sentence splitting if NLTK fails
            sentences = text.split('. ')
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < 500:  # Max chunk size
                current_chunk += sentence + " "
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # Create embeddings for chunks
        embeddings = self.embedder.encode(chunks)
        for i, chunk in enumerate(chunks):
            self.collection.add(
                documents=[chunk],
                embeddings=[embeddings[i]],
                metadatas=[metadata],
                ids=[f"{metadata.get('filename', 'doc')}_{i}"]
            )

    def parse_query_llm(self, query):
        prompt = f"""
You are an expert insurance document analyzer. Extract the key information from this query and structure it for analysis.

Query: "{query}"

Extract the following information:
- Main topic (e.g., grace period, waiting period, coverage, etc.)
- Specific details mentioned
- Type of information being requested

Return ONLY a JSON object with these fields:
{{
    "topic": "main topic of the query",
    "details": "specific details mentioned",
    "request_type": "what type of information is being requested"
}}

Example for "What is the grace period for premium payment?":
{{
    "topic": "grace period",
    "details": "premium payment",
    "request_type": "policy terms and conditions"
}}

Respond ONLY with valid JSON, no extra text.
"""
        response = call_ollama(prompt)
        json_str = self.extract_json(response)
        try:
            parsed = json.loads(json_str)
        except Exception:
            parsed = {"topic": "general", "details": query, "request_type": "information"}
        return parsed

    def process_query(self, query, top_k=8):
        # Parse the query to understand what's being asked
        parsed_query = self.parse_query_llm(query)
        
        # Create query embedding
        query_embedding = self.embedder.encode([query])[0]
        
        # Retrieve relevant chunks
        results = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        retrieved_chunks = results['documents'][0]
        
        # Enhanced reasoning prompt
        reasoning_prompt = f"""
You are an expert insurance policy analyst. Analyze the following query and relevant document clauses to provide a comprehensive answer.

QUERY: "{query}"

PARSED QUERY INFO:
- Topic: {parsed_query.get('topic', 'general')}
- Details: {parsed_query.get('details', 'none')}
- Request Type: {parsed_query.get('request_type', 'information')}

RELEVANT DOCUMENT CLAUSES:
"""
        
        for idx, clause in enumerate(retrieved_chunks):
            reasoning_prompt += f"{idx}: \"{clause}\"\n"
        
        reasoning_prompt += f"""
TASK: Provide a direct, concise answer to the query based on the relevant clauses above.

REQUIREMENTS:
1. Answer the SPECIFIC question asked in 1-2 sentences maximum
2. Include only the most important details (numbers, time periods, conditions)
3. If information is not found, simply state "Information not available in the policy document"
4. Be direct and to the point

RESPONSE FORMAT (JSON only):
{{
    "answer": "direct answer in 1-2 sentences",
    "summary": "brief summary in 3-5 words",
    "relevant_clauses": [list of clause numbers that support the answer],
    "source_text": "exact text from relevant clauses",
    "confidence": "high/medium/low based on available information"
}}

IMPORTANT: 
- Keep answers SHORT and DIRECT
- Answer ONLY the question asked
- Do NOT mention "the user asked" or "based on chunks"
- Do NOT explain what you're doing
- Just give the direct answer
- Respond ONLY with valid JSON, no extra text
"""
        
        llm_response = call_ollama(reasoning_prompt)
        json_str = self.extract_json(llm_response)
        
        try:
            if json_str is None:
                raise ValueError("No valid JSON found in LLM response")
            
            result = json.loads(json_str)
            # Ensure we have the required fields
            if 'answer' not in result:
                result['answer'] = "Unable to provide a specific answer based on the available information."
            if 'summary' not in result:
                result['summary'] = result.get('answer', 'No summary available.')
            if 'relevant_clauses' not in result:
                result['relevant_clauses'] = []
            if 'source_text' not in result:
                result['source_text'] = ""
            if 'confidence' not in result:
                result['confidence'] = "low"
                
        except Exception as e:
            # Pure AI fallback - let the LLM try to generate a response from the retrieved chunks
            fallback_prompt = f"""
You are an expert insurance policy analyst. The user asked: "{query}"

Here are the relevant document chunks that were found:
"""
            for idx, chunk in enumerate(retrieved_chunks):
                fallback_prompt += f"{idx}: \"{chunk}\"\n"
            
            fallback_prompt += f"""
Based on these chunks, provide a DIRECT answer to the user's question in 1-2 sentences maximum.

IMPORTANT: 
- Answer ONLY the question asked
- Do NOT mention "the user asked" or "based on chunks"
- Do NOT explain what you're doing
- Just give the direct answer

If the information is not available, simply say "Information not available in the policy document."
"""
            
            try:
                fallback_response = call_ollama(fallback_prompt)
                answer = fallback_response.strip()
                summary = "Generated from retrieved document chunks"
                confidence = "medium"
                source_text = "; ".join([f"Clause {i}: {chunk[:100]}..." for i, chunk in enumerate(retrieved_chunks[:3])])
                relevant_clauses = list(range(len(retrieved_chunks)))
            except Exception as fallback_error:
                # If even the fallback fails, provide a basic response
                answer = f"Based on the policy document, I found some relevant information but cannot provide a complete answer to: {query}"
                summary = "Information partially available"
                confidence = "low"
                source_text = ""
                relevant_clauses = []
            
            result = {
                'answer': answer,
                'summary': summary,
                'relevant_clauses': relevant_clauses,
                'source_text': source_text,
                'confidence': confidence,
                'error': str(e)
            }
        
        # Add the retrieved chunks for reference
        result['retrieved_chunks'] = retrieved_chunks
        
        return result

    @staticmethod
    def extract_json(text):
        # Improved JSON extraction with better patterns
        if not text:
            return None
            
        # Clean the text first
        text = text.strip()
        
        # Look for JSON objects with proper structure
        json_patterns = [
            r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Nested JSON
            r'\{[^}]*\}',  # Simple JSON
            r'\{[^}]*"[^"]*"[^}]*\}',  # JSON with quoted strings
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                try:
                    # Clean the match
                    cleaned_match = match.strip()
                    # Test if it's valid JSON
                    json.loads(cleaned_match)
                    return cleaned_match
                except:
                    continue
        
        # If no valid JSON found, try to extract key-value pairs manually
        try:
            # Look for common patterns in the response
            answer_match = re.search(r'"answer"\s*:\s*"([^"]*)"', text, re.IGNORECASE)
            summary_match = re.search(r'"summary"\s*:\s*"([^"]*)"', text, re.IGNORECASE)
            confidence_match = re.search(r'"confidence"\s*:\s*"([^"]*)"', text, re.IGNORECASE)
            
            if answer_match or summary_match:
                result = {}
                if answer_match:
                    result['answer'] = answer_match.group(1)
                if summary_match:
                    result['summary'] = summary_match.group(1)
                if confidence_match:
                    result['confidence'] = confidence_match.group(1)
                else:
                    result['confidence'] = 'medium'
                
                result['relevant_clauses'] = []
                result['source_text'] = ""
                
                return json.dumps(result)
        except:
            pass
        
        return None 