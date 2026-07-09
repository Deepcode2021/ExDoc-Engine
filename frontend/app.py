
import streamlit as st
import requests

# 1. Page Configuration (Must be the very first Streamlit command)
st.set_page_config(page_title="Self-Hosted Document Extraction API v1", layout="wide")

st.title("📄 Self-Hosted Document Extraction Engine API")
st.write("Upload any document (PDF, DOCX, XLSX, PPTX) to extract layout,content clean Markdown.")
st.write("Created by DeepCode")

# 2. Network Endpoint Definition
# When running locally, this hits your machine's localhost. 
# (When we move to Docker Compose later, this will change to http://backend:8000/extract)
BACKEND_URL = "http://127.0.0.1:8000/extract"

# 3. File Upload Widget
uploaded_file = st.file_uploader(
    "Choose a document", 
    type=["pdf", "docx", "xlsx", "pptx", "txt", "html"]
)

# 4. Processing Action Trigger
if uploaded_file is not None:
    if st.button("Extract Content"):
        with st.spinner("Processing document through extraction pipelines..."):
            
            # Package the file binary data into a standard multipart form payload
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            }
            
            try:
                # Send the POST request to the FastAPI backend
                response = requests.post(BACKEND_URL, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Successfully processed using **{data['engine']}**!")
                    
                    # Display the results in layout tabs
                    tab1, tab2 = st.tabs(["Markdown Preview", "Raw Code / Payload"])
                    
                    with tab1:
                        st.markdown(data["content"])
                        
                    with tab2:
                        st.code(data["content"], language="markdown")
                else:
                    st.error(f"Backend Error: {response.text}")
                    
            except Exception as e:
                st.error(f"Could not connect to backend API: {e}")