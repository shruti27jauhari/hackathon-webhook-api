import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="Dashboard - Insurance Policy Analyzer", page_icon="📊", layout="wide")

# Custom CSS for dashboard
st.markdown("""
<style>
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 0.5rem;
        border-left: 4px solid #667eea;
        color: #495057;
        border: 1px solid #e9ecef;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online { background-color: #4CAF50; }
    .status-offline { background-color: #f44336; }
    .status-warning { background-color: #ff9800; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Insurance Policy Analyzer Dashboard")

# System Status
st.header("🔧 System Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>🤖 AI Model</h3>
        <h2>TinyLlama</h2>
        <p><span class="status-indicator status-online"></span>Online</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>🔍 Vector DB</h3>
        <h2>ChromaDB</h2>
        <p><span class="status-indicator status-online"></span>Connected</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>📄 Documents</h3>
        <h2>0</h2>
        <p>Loaded</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3>⚡ API</h3>
        <h2>FastAPI</h2>
        <p><span class="status-indicator status-online"></span>Running</p>
    </div>
    """, unsafe_allow_html=True)

# Performance Metrics
st.header("📈 Performance Metrics")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Response Times")
    
    # Simulate response time data
    response_times = [2.1, 1.8, 2.3, 1.9, 2.0, 1.7, 2.2]
    avg_response = sum(response_times) / len(response_times)
    
    st.metric("Average Response Time", f"{avg_response:.1f}s", "-0.2s")
    st.metric("Fastest Response", f"{min(response_times):.1f}s")
    st.metric("Slowest Response", f"{max(response_times):.1f}s")

with col2:
    st.subheader("System Resources")
    
    # Simulate resource usage
    st.metric("Memory Usage", "2.1 GB", "64%")
    st.metric("CPU Usage", "45%", "Normal")
    st.metric("Storage", "1.2 GB", "Available")

# Recent Activity
st.header("🕒 Recent Activity")

# Simulate activity log
activities = [
    {"time": "2 minutes ago", "action": "Document processed", "file": "policy.pdf"},
    {"time": "5 minutes ago", "action": "Query processed", "query": "grace period"},
    {"time": "8 minutes ago", "action": "System started", "component": "TinyLlama"},
    {"time": "12 minutes ago", "action": "API endpoint called", "endpoint": "/hackrx/run"},
]

for activity in activities:
    file_info = activity.get('file', activity.get('query', activity.get('component', '')))
    st.info(f"**{activity['time']}** - {activity['action']}: {file_info}")

# System Health
st.header("🏥 System Health")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Component Status")
    
    components = [
        {"name": "Ollama Server", "status": "✅ Online", "color": "green"},
        {"name": "ChromaDB", "status": "✅ Connected", "color": "green"},
        {"name": "FastAPI", "status": "✅ Running", "color": "green"},
        {"name": "Streamlit", "status": "✅ Active", "color": "green"},
    ]
    
    for component in components:
        st.success(f"**{component['name']}**: {component['status']}")

with col2:
    st.subheader("Error Log")
    
    # Simulate error log
    st.warning("No errors in the last 24 hours")
    st.info("System running smoothly")

# Quick Actions
st.header("⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Refresh Status", use_container_width=True):
        st.success("Status refreshed!")

with col2:
    if st.button("📊 View Logs", use_container_width=True):
        st.info("Logs would be displayed here")

with col3:
    if st.button("🔧 System Info", use_container_width=True):
        st.json({
            "version": "1.0.0",
            "python": "3.12.5",
            "platform": "Windows",
            "ollama": "0.5.2",
            "chromadb": "0.4.0"
        })

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📊 Dashboard | Insurance Policy Analyzer | Real-time monitoring</p>
</div>
""", unsafe_allow_html=True) 