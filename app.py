import streamlit as st
import json
from document_loader import extract_text_from_pdf, extract_text_from_docx, extract_text_from_eml
from rag_engine import RAGEngine

# Page configuration
st.set_page_config(
    page_title="Insurance Policy Analyzer",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        color: #495057;
    }
    
    .status-success {
        background: linear-gradient(90deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        border: 1px solid #c3e6cb;
    }
    
    .status-info {
        background: linear-gradient(90deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        border: 1px solid #bee5eb;
    }
    
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f8f9fa;
        margin: 1rem 0;
    }
    
    .query-box {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        color: #495057;
        border: 1px solid #e9ecef;
    }
    
    .response-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #495057;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #667eea;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 0.5rem;
        color: #495057;
        border: 1px solid #e9ecef;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Ensure all text is visible */
    .stMarkdown, .stText, .stTextInput, .stTextArea {
        color: #495057 !important;
    }
    
    /* Better contrast for success/error messages */
    .stSuccess {
        background-color: #d4edda !important;
        color: #155724 !important;
        border: 1px solid #c3e6cb !important;
    }
    
    .stError {
        background-color: #f8d7da !important;
        color: #721c24 !important;
        border: 1px solid #f5c6cb !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        color: #856404 !important;
        border: 1px solid #ffeaa7 !important;
    }
    
    .stInfo {
        background-color: #d1ecf1 !important;
        color: #0c5460 !important;
        border: 1px solid #bee5eb !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📋 Insurance Policy Analyzer</h1>
    <p>Intelligent Document Analysis & Query Processing</p>
</div>
""", unsafe_allow_html=True)

# Initialize RAGEngine in session state
if 'rag' not in st.session_state:
    st.session_state['rag'] = RAGEngine()
if 'loaded_docs' not in st.session_state:
    st.session_state['loaded_docs'] = set()
if 'doc_processing' not in st.session_state:
    st.session_state['doc_processing'] = False
if 'ready' not in st.session_state:
    st.session_state['ready'] = False

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 10px; color: white; margin-bottom: 2rem; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
        <h3>📄 Document Upload</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader with better styling
    st.markdown("### Upload Documents")
    doc_files = st.file_uploader(
        'Choose files',
        type=['pdf', 'docx', 'eml'],
        accept_multiple_files=True,
        help="Upload PDF, Word, or Email files for analysis"
    )
    
    # Document processing status
    if doc_files:
        st.markdown("### 📊 Processing Status")
        with st.spinner('Processing documents...'):
            for file in doc_files:
                if file.name in st.session_state['loaded_docs']:
                    st.success(f"✅ {file.name} (already processed)")
                    continue
                
                st.info(f"🔄 Processing {file.name}...")
                
                try:
                    if file.type == 'application/pdf':
                        text = extract_text_from_pdf(file)
                    elif file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                        text = extract_text_from_docx(file)
                    elif file.type == 'message/rfc822' or file.name.endswith('.eml'):
                        text = extract_text_from_eml(file)
                    else:
                        st.warning(f'⚠️ Unsupported file type: {file.name}')
                        continue
                    
                    st.session_state['rag'].add_document(text, {'filename': file.name})
                    st.session_state['loaded_docs'].add(file.name)
                    st.success(f"✅ {file.name} processed successfully")
                    
                except Exception as e:
                    st.error(f"❌ Error processing {file.name}: {str(e)}")
    
    # System status
    st.markdown("### 🔧 System Status")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Documents Loaded", len(st.session_state['loaded_docs']))
    
    with col2:
        if st.session_state['ready']:
            st.metric("Status", "✅ Ready", delta="Active")
        else:
            st.metric("Status", "⏳ Waiting", delta="Inactive")
    
    # Features info
    st.markdown("### ✨ Features")
    st.markdown("""
    - 📄 **Multi-format Support**: PDF, DOCX, Email
    - 🔍 **Semantic Search**: Advanced document retrieval
    - 🤖 **AI-Powered**: Local LLM processing
    - 📊 **Structured Output**: JSON responses
    - 🔒 **Privacy-First**: All processing local
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Query section
    st.markdown("""
    <div class="query-box">
        <h2>🔍 Ask Your Questions</h2>
        <p>Enter natural language queries about your uploaded documents.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Query input
    query = st.text_area(
        "Enter your query",
        placeholder="e.g., 'What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?'",
        height=100,
        help="Ask questions about your uploaded documents"
    )
    
    # Submit button
    col_submit1, col_submit2, col_submit3 = st.columns([1, 2, 1])
    with col_submit2:
        submit_button = st.button("🚀 Process Query", use_container_width=True)
    
    # Process query
    if submit_button and query:
        if not st.session_state['loaded_docs']:
            st.error("⚠️ Please upload documents first before processing queries.")
        else:
            with st.spinner("🤖 Processing your query..."):
                try:
                    response = st.session_state['rag'].process_query(query)
                    
                    # Display results
                    st.markdown("""
                    <div class="response-box">
                        <h3>📝 Analysis Results</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Main Answer
                    if 'answer' in response and response['answer']:
                        st.markdown(f"""
                        <div class="status-success">
                            <h4>💡 Answer</h4>
                            <p>{response['answer']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Summary
                    if 'summary' in response and response['summary']:
                        st.markdown(f"""
                        <div class="feature-card">
                            <h4>📋 Summary</h4>
                            <p>{response['summary']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Confidence Level
                    if 'confidence' in response:
                        confidence_emoji = "🟢" if response['confidence'] == 'high' else "🟡" if response['confidence'] == 'medium' else "🔴"
                        st.markdown(f"""
                        <div class="feature-card">
                            <h4>{confidence_emoji} Confidence Level</h4>
                            <p>{response['confidence'].upper()}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Source Text
                    if 'source_text' in response and response['source_text']:
                        st.markdown(f"""
                        <div class="feature-card">
                            <h4>📄 Source Information</h4>
                            <p>{response['source_text']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Relevant Clauses
                    if 'relevant_clauses' in response and response['relevant_clauses']:
                        st.markdown(f"""
                        <div class="feature-card">
                            <h4>🔗 Relevant Clauses</h4>
                            <p>Clauses referenced: {', '.join(map(str, response['relevant_clauses']))}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Full JSON response (collapsible)
                    with st.expander("🔧 Technical Details (JSON Response)"):
                        st.json(response)
                        
                except Exception as e:
                    st.error(f"❌ Error processing query: {str(e)}")
                    st.info("💡 Try rephrasing your question or check if documents are properly loaded.")

with col2:
    # Quick stats
    st.markdown("### 📊 Quick Stats")
    
    if st.session_state['loaded_docs']:
        st.markdown(f"""
        <div class="metric-card">
            <h4>📄 Documents</h4>
            <h2>{len(st.session_state['loaded_docs'])}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h4>🤖 AI Model</h4>
            <h2>TinyLlama</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <h4>🔍 Vector DB</h4>
            <h2>ChromaDB</h2>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("📄 Upload documents to see statistics")
    
    # Sample queries
    st.markdown("### 💡 Sample Queries")
    sample_queries = [
        "What is the grace period for premium payment?",
        "Does this policy cover maternity expenses?",
        "What is the waiting period for pre-existing diseases?",
        "Are organ donor expenses covered?",
        "What is the No Claim Discount (NCD)?"
    ]
    
    for i, sample in enumerate(sample_queries):
        if st.button(f"💬 {sample[:30]}...", key=f"sample_{i}"):
            st.session_state['sample_query'] = sample
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📋 Powered by Insurance Policy Analyzer | Local AI Processing | Privacy-First Design</p>
</div>
""", unsafe_allow_html=True) 