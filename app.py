import streamlit as st
from langchain_community.llms import HuggingFaceHub
import os
from fpdf import FPDF
from io import BytesIO
import textwrap
import re

# Page setup + dark theme
st.set_page_config(page_title="Pro Competitive Analysis", layout="centered")
st.markdown("""
<style>
body {
    background-color: #111 !important;
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #ffffff;
}
textarea, input, button, .stTextInput>div>div>input {
    background-color: #1c1c1c !important;
    color: #f1f1f1 !important;
    border: 1px solid #444 !important;
}
button:hover {
    background-color: #444 !important;
}
.stDownloadButton>button {
    background-color: #222 !important;
    color: white;
}
.stDownloadButton>button:hover {
    background-color: #444 !important;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("💼 Competitive Analysis Pro")
st.markdown("Get an expert-level markdown analysis between two products or services, including SWOT, features, and recommendations.")

# Set Hugging Face token
os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["HF_TOKEN"]

# Load Mistral LLM (Free model)
llm = HuggingFaceHub(
    repo_id="mistralai/Mistral-7B-Instruct-v0.1",
    model_kwargs={"temperature": 0.7, "max_new_tokens": 1024}
)

# Inputs
product1 = st.text_area("🧩 Product/Service 1", height=200, placeholder="e.g., iPhone 13")
product2 = st.text_area("🧩 Product/Service 2", height=200, placeholder="e.g., iPhone 14")

# Compare
if st.button("🔍 Run Competitive Analysis", use_container_width=True):
    if not product1 or not product2:
        st.warning("Please enter both product descriptions.")
    else:
        with st.spinner("🧠 Generating insights with Mistral..."):
            prompt = f"""
Compare the following two products or services:
Product 1:
{product1}
Product 2:
{product2}
Return a professional analysis in markdown format that includes:
- Feature-by-feature comparison
- SWOT analysis for each product
- Business use cases and recommendations
- Key differentiators and which product suits which audience
Do NOT include or mention these instructions.
Only return the clean markdown report.
"""
            result = llm(prompt)

        # Display output
        st.markdown("### 📊 Expert Comparison")
        st.markdown(result)
