"""ProjectForge - Streamlit Web UI

Web interface for the ProjectForge AI-powered business analysis tool.
"""

import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

from project_forge.core import run_analysis_workflow
from project_forge.utils.exporters import generate_text_content, generate_pdf_bytes

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ProjectForge - AI Business Analyst",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Font Awesome icons
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #fafafa !important;
    }
    .status-success {
        color: #27ae60;
        font-weight: bold;
    }
    .status-error {
        color: #e74c3c;
        font-weight: bold;
    }
    .icon {
        margin-right: 8px;
    }
    /* Prevent content overflow only where needed */
    .stMarkdown table {
        max-width: 100%;
        display: block;
        overflow-x: auto;
    }
    .stMarkdown img {
        max-width: 100%;
        height: auto;
    }
    .stMarkdown pre {
        max-width: 100%;
        overflow-x: auto;
    }
    /* Fix h3 visibility in dark mode */
    h3 {
        color: #fafafa !important;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'text_output' not in st.session_state:
        st.session_state.text_output = None
    if 'pdf_bytes' not in st.session_state:
        st.session_state.pdf_bytes = None


def run_analysis(user_input: str, model_name: str, api_key: str):
    """Execute the analysis workflow and store results in session state."""
    with st.spinner("🔄 Running AI analysis workflow... This may take a few minutes."):
        # Run workflow (interactive_mode=False for web UI)
        result = run_analysis_workflow(
            user_input=user_input,
            llm_model=model_name,
            api_key=api_key,
            interactive_mode=False
        )
        
        # Store result in session state
        st.session_state.result = result
        st.session_state.analysis_complete = True
        
        # Generate text output
        if result['success']:
            outputs = result['outputs']
            st.session_state.text_output = generate_text_content(
                timestamp=result['timestamp'],
                user_input=user_input,
                ba_output=outputs['intake'],
                architect_output=outputs['architect'],
                qa_output=outputs['quality'],
                synthesis_output=outputs['synthesis'],
                pm_output=outputs['manager']
            )
            
            # Generate PDF
            try:
                st.session_state.pdf_bytes = generate_pdf_bytes(result['html_content'])
            except Exception as pdf_error:
                st.warning(f"PDF generation failed: {pdf_error}")
                st.session_state.pdf_bytes = None


def display_results():
    """Display analysis results in the UI."""
    result = st.session_state.result
    
    if not result:
        return
    
    # Display status
    if result['success']:
        st.markdown('<p class="status-success"><i class="fas fa-check-circle icon"></i>Analysis Complete!</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="status-error"><i class="fas fa-exclamation-triangle icon"></i>Workflow Error: {result["error"]}</p>', unsafe_allow_html=True)
        st.info("Partial results may be available below.")
    
    # Display agent outputs in expandable sections
    outputs = result['outputs']
    
    st.markdown('<div class="section-header"><i class="fas fa-tasks icon"></i>Agent Analysis Results</div>', unsafe_allow_html=True)
    
    with st.expander("1. Requirements Intake Specialist", expanded=True):
        st.markdown(outputs['intake'] or "*Task did not complete*")
    
    with st.expander("2. Solution Architect"):
        st.markdown(outputs['architect'] or "*Task did not complete*")
    
    with st.expander("3. Quality Assurance Specialist"):
        st.markdown(outputs['quality'] or "*Task did not complete*")
    
    with st.expander("4. Synthesis Specialist"):
        st.markdown(outputs['synthesis'] or "*Task did not complete*")
    
    with st.expander("5. Project Manager"):
        st.markdown(outputs['manager'] or "*Task did not complete*")
    
    # Download section
    st.markdown('<div class="section-header"><i class="fas fa-download icon"></i>Download Results</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    timestamp = result['timestamp']
    
    with col1:
        if st.session_state.text_output:
            st.download_button(
                label="TXT",
                data=st.session_state.text_output,
                file_name=f"output_{timestamp}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with col2:
        if result['html_content']:
            st.download_button(
                label="HTML",
                data=result['html_content'],
                file_name=f"output_{timestamp}.html",
                mime="text/html",
                use_container_width=True
            )
    
    with col3:
        if st.session_state.pdf_bytes:
            st.download_button(
                label="PDF",
                data=st.session_state.pdf_bytes,
                file_name=f"output_{timestamp}.pdf",
                mime="application/pdf",
                use_container_width=True
            )


def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header"><i class="fas fa-rocket icon"></i>ProjectForge</div>', unsafe_allow_html=True)
    st.markdown("### AI-Powered Business Analysis Tool")
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Model selection
        model_name = st.text_input(
            "LLM Model",
            value=os.getenv("LLM_MODEL", "gemini/gemini-2.5-flash"),
            help="Specify the LLM model to use for analysis"
        )
        
        # API key
        api_key = st.text_input(
            "Google API Key",
            value=os.getenv("GOOGLE_API_KEY", ""),
            type="password",
            help="Your Google API key for Gemini models"
        )
        
        if not api_key:
            st.warning("Please provide a Google API key to proceed.")
        
        st.markdown("---")
        st.markdown("**About ProjectForge**")
        st.markdown(
            "ProjectForge uses a team of 5 AI agents to analyze your "
            "project idea and generate a comprehensive business plan."
        )
    
    # Main input area
    st.markdown("### Describe Your Project Idea")
    
    user_input = st.text_area(
        "Project Description",
        height=150,
        placeholder="Example: A mobile app for tracking daily water intake with reminders and progress visualization...",
        help="Describe your project idea, features, constraints, or just a general concept."
    )
    
    # Run analysis button
    if st.button("Run Analysis", type="primary", disabled=not api_key or not user_input):
        if user_input:
            run_analysis(user_input, model_name, api_key)
        else:
            st.warning("Please enter a project description.")
    
    # Display results if analysis is complete
    if st.session_state.analysis_complete:
        st.markdown("---")
        display_results()


if __name__ == "__main__":
    main()
