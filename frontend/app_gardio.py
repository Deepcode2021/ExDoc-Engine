# frontend/app.py
import streamlit as st
import os
from gradio_client import Client, handle_file

st.set_page_config(page_title="Universal Extractor UI", layout="wide")

st.title("📄 Self-Hosted Document Extraction Engine API")
st.write("Upload any document (PDF, DOCX, XLSX, PPTX) to extract layout,content clean Markdown.")
st.write("Created by DeepCode")

# Initialize the cloud client
# Replace with your actual Hugging Face username and Space name
# Initialize the cloud client with authentication
HF_API_URL = "kyakaruiska/Extraction_API" 

# Replace the string below with your actual token
HF_TOKEN = os.getenv("HF_TOKEN") 
if not HF_TOKEN:
    st.error("❌ Environment variable 'HF_TOKEN' not found! Please set it in your terminal before running the app.")
    st.stop()

client = Client(HF_API_URL, token=HF_TOKEN)

uploaded_file = st.file_uploader("Choose a document", type=["pdf", "docx", "xlsx", "pptx", "txt", "html"])

if uploaded_file is not None:
    if st.button("Extract Content"):
        # 1. Use st.status instead of st.spinner for multi-step feedback
        with st.status("Connecting to Cloud API...", expanded=True) as status:
            temp_path = os.path.join(os.getcwd(), uploaded_file.name)
            
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            try:
                # The Gradio API requires 'handle_file' to stream binary data securely
                result = client.predict(
                    uploaded_file=handle_file(temp_path),
                    fn_index=0  # Targets the first (and only) function in your Gradio setup
                )
                
                st.success("Successfully processed via Cloud API!")
                
                # 'result' contains the markdown string output from Hugging Face
                tab1, tab2 = st.tabs(["Markdown Preview", "Raw Code / Payload"])
                
                with tab1:
                    st.markdown(result)
                with tab2:
                    st.code(result, language="markdown")
                    
            except Exception as e:
                st.error(f"Cloud API Error: {e}")
                
            finally:
                # Clean up local temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

