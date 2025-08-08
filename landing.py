import streamlit as st
import time

# Page configuration
st.set_page_config(
    page_title="HackRX RAG System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for landing page
st.markdown("""
<style>
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.3s ease;
        border-top: 4px solid #667eea;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .cta-button {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem 3rem;
        border-radius: 50px;
        text-decoration: none;
        display: inline-block;
        font-weight: bold;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    .tech-stack {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
    }
    
    .tech-item {
        display: inline-block;
        background: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        font-weight: bold;
        color: #667eea;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section fade-in">
    <h1 style="font-size: 3.5rem; margin-bottom: 1rem;">🤖 HackRX RAG System</h1>
    <p style="font-size: 1.5rem; margin-bottom: 2rem;">Intelligent Document Analysis & Query Processing</p>
    <p style="font-size: 1.1rem; opacity: 0.9;">Advanced LLM-Powered Retrieval System for Insurance, Legal, HR, and Compliance Domains</p>
</div>
""", unsafe_allow_html=True)

# Features Grid
st.markdown("### ✨ Key Features")
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <h3>📄 Multi-Format Support</h3>
        <p>Process PDFs, Word documents, and emails with advanced text extraction</p>
        <div style="font-size: 2rem;">📄📝📧</div>
    </div>
    
    <div class="feature-card">
        <h3>🔍 Semantic Search</h3>
        <p>Advanced vector-based retrieval using ChromaDB for precise document matching</p>
        <div style="font-size: 2rem;">🔍📊</div>
    </div>
    
    <div class="feature-card">
        <h3>🤖 AI-Powered Analysis</h3>
        <p>Local TinyLlama model for intelligent query processing and decision making</p>
        <div style="font-size: 2rem;">🤖🧠</div>
    </div>
    
    <div class="feature-card">
        <h3>📊 Structured Output</h3>
        <p>JSON responses with explainable decisions and clause references</p>
        <div style="font-size: 2rem;">📊📋</div>
    </div>
    
    <div class="feature-card">
        <h3>🔒 Privacy-First</h3>
        <p>All processing happens locally - no data leaves your machine</p>
        <div style="font-size: 2rem;">🔒🛡️</div>
    </div>
    
    <div class="feature-card">
        <h3>⚡ Real-Time Processing</h3>
        <p>Fast response times with optimized token usage and efficient retrieval</p>
        <div style="font-size: 2rem;">⚡🚀</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Statistics
st.markdown("### 📈 System Capabilities")
st.markdown("""
<div class="stats-container">
    <div class="stat-card">
        <h3>🎯 Accuracy</h3>
        <h2>High Precision</h2>
        <p>Advanced clause matching</p>
    </div>
    
    <div class="stat-card">
        <h3>⚡ Latency</h3>
        <h2>Fast Response</h2>
        <p>Real-time processing</p>
    </div>
    
    <div class="stat-card">
        <h3>🔧 Efficiency</h3>
        <h2>Optimized</h2>
        <p>Token-efficient usage</p>
    </div>
    
    <div class="stat-card">
        <h3>🔄 Reusability</h3>
        <h2>Modular</h2>
        <p>Extensible architecture</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Technical Stack
st.markdown("### 🛠️ Technical Stack")
st.markdown("""
<div class="tech-stack">
    <div style="text-align: center; margin-bottom: 1rem;">
        <h4>Built with cutting-edge technologies</h4>
    </div>
    <div style="text-align: center;">
        <span class="tech-item">FastAPI</span>
        <span class="tech-item">ChromaDB</span>
        <span class="tech-item">TinyLlama</span>
        <span class="tech-item">Sentence Transformers</span>
        <span class="tech-item">Streamlit</span>
        <span class="tech-item">Python</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Use Cases
st.markdown("### 🎯 Use Cases")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🏥 Insurance</h3>
        <ul>
            <li>Policy analysis and claims processing</li>
            <li>Coverage determination</li>
            <li>Premium calculation queries</li>
            <li>Exclusion clause identification</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>⚖️ Legal & Compliance</h3>
        <ul>
            <li>Contract analysis and review</li>
            <li>Regulatory compliance checking</li>
            <li>Legal document search</li>
            <li>Clause interpretation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Call to Action
st.markdown("### 🚀 Get Started")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style="text-align: center;">
        <a href="/app" class="cta-button">🚀 Launch Application</a>
        <p style="margin-top: 1rem; color: #666;">Experience the power of intelligent document analysis</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🤖 HackRX RAG System | Powered by Local AI | Privacy-First Design</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">Built for the HackRX Hackathon | Advanced LLM-Powered Query-Retrieval System</p>
</div>
""", unsafe_allow_html=True) 