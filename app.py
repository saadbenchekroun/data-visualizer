import streamlit as st
import pandas as pd
import os
from utils.data_processor import list_uploaded_files

# Configure page settings
st.set_page_config(
    page_title="DataVizSME - Smart Visualization Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {}  # {filename: df}
if 'current_file' not in st.session_state:
    st.session_state.current_file = None
if 'visualizations' not in st.session_state:
    st.session_state.visualizations = {}  # {viz_name: {config}}
if 'active_integrations' not in st.session_state:
    st.session_state.active_integrations = {}  # {integration_name: status}

# Main page content
st.title("📊 DataVizSME - Data Visualization Platform for SMEs")
st.subheader("Welcome to your business intelligence dashboard")

# Dashboard overview
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Datasets", value=len(st.session_state.uploaded_files))
    
with col2:
    st.metric(label="Visualizations", value=len(st.session_state.visualizations))
    
with col3:
    st.metric(label="Active Integrations", value=len(st.session_state.active_integrations))

# Recent activity section
st.subheader("Recent Activity")

# Display recent datasets
if st.session_state.uploaded_files:
    st.write("📁 Recent Datasets:")
    files = list_uploaded_files()
    if files:
        for i, file in enumerate(files[:3]):  # Show last 3 files
            st.write(f"- {file}")
    else:
        st.write("No datasets uploaded yet.")
else:
    st.info("👋 Get started by uploading data in the Data Upload section")
    
# Quick actions
st.subheader("Quick Actions")
quick_actions = st.columns(4)

with quick_actions[0]:
    if st.button("📤 Upload Data"):
        st.switch_page("pages/1_Data_Upload.py")
        
with quick_actions[1]:
    if st.button("📊 Create Visualization"):
        st.switch_page("pages/2_Data_Visualization.py")
        
with quick_actions[2]:
    if st.button("📋 Browse Templates"):
        st.switch_page("pages/3_Templates.py")
        
with quick_actions[3]:
    if st.button("🔗 Setup Integrations"):
        st.switch_page("pages/4_Integrations.py")

# Feature overview
st.subheader("Platform Features")

features = {
    "Natural Language Queries": "Ask questions about your data in plain English",
    "Industry Templates": "Pre-built visualizations for common business needs",
    "External Tool Integration": "Connect with QuickBooks, Shopify, and more",
    "Drag-and-Drop Interface": "Create visualizations without coding"
}

for feature, description in features.items():
    st.write(f"**{feature}**: {description}")

# Footer
st.markdown("---")
st.caption("DataVizSME - Making business intelligence accessible for small and medium enterprises")
