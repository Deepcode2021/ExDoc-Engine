# ExDoc-Engine
# 📄 Self-Hosted Document Extraction Engine

An advanced, layout-aware document extraction API and dashboard. This tool intelligently routes documents to specialised machine learning models to extract highly structured Markdown, preserving headings, tables, and natively embedding images.

## ✨ Features

* **Visual PDF Extraction:** Uses **IBM Docling** to analyze page layouts. It doesn't just scrape text; it understands column structures,table matrices and extracts images as embedded Base64 Markdown (`![image](data:image...)`).
* **Native Office Support:** Uses **Microsoft MarkItDown** for lightning-fast, highly accurate extraction of text from Word (`.docx`), Excel (`.xlsx`), and PowerPoint (`.pptx`) files.
* **Cloud GPU Accelerated:** The frontend is configured to securely stream documents to a Hugging Face ZeroGPU endpoint, keeping your local machine fast and lightweight.
* **Semantic Chunking (Local Backend):** Includes an advanced `/extract/chunks` API endpoint for RAG pipelines to split documents strictly by layout boundaries instead of blind character counts.

## 🛠️ Technology Stack

* **Frontend:** Streamlit, Gradio Python Client
* **AI & Parsing Engines:** IBM Docling (v2.0), Microsoft MarkItDown
* **Cloud Infrastructure:** Hugging Face Spaces (ZeroGPU)
* **Local Backend Framework:** FastAPI, Uvicorn

## 🚀 Getting Started (Local Streamlit UI)

To run the interactive extraction dashboard on your local machine:

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/universal-extractor.git](https://github.com/yourusername/universal-extractor.git)
cd universal-extractor
