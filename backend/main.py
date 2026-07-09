import os 
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from docling.document_converter import DocumentConverter
from markitdown import MarkItDown
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.chunking import HybridChunker
from docling.datamodel.base_models import InputFormat, ImageRefMode


app = FastAPI(
    title="Self-Hosted Document Extraction API",
    description="This is Document parsing engine using IBM Docling and MarkItDown"
)

docling_converter = DocumentConverter()

# FOR THE IMAGE EXTRACTION ||||||

pipeline_options = PdfPipelineOptions()
pipeline_options.generate_picture_images = True  # Capture images/diagrams
pipeline_options.images_scale = 2.0             # High resolution scale multiplier
pipeline_options.do_picture_description = True # Turn on automatic visual asset descriptions

format_options = {
    InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
}
# 3. Pass options to the constructor
docling_converter = DocumentConverter(format_options=format_options)
markitdown_converter = MarkItDown()

#for the temp files :)
UPLOAD_DIR = "/tmp/extracted_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/extract")
async def extract_document(file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1].lower()
    temp_file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        if file_ext == ".pdf":
            # Pass to IBM Docling
            result = docling_converter.convert(temp_file_path)
            # Instruct the exporter to embed image artifacts seamlessly into the MD text string
            extracted_text = result.document.export_to_markdown(image_mode=ImageRefMode.EMBEDDED)
            engine_used = "IBM Docling"
            
        elif file_ext in [".docx", ".xlsx", ".pptx", ".html", ".txt", ".md"]:
            # Pass to Microsoft MarkItDown
            result = markitdown_converter.convert(temp_file_path)
            extracted_text = result.text_content
            engine_used = "Microsoft MarkItDown"
            
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {file_ext}")

        return {
            "filename": file.filename,
            "engine": engine_used,
            "content": extracted_text
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
        
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# --- ENDPOINT 2: SEMANTIC CHUNKER FOR AI/RAG ---
@app.post("/extract/chunks")
async def extract_chunks(file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    # Semantic chunking relies heavily on layout structures. We restrict this to PDFs.
    if file_ext != ".pdf":
        raise HTTPException(status_code=400, detail="Semantic chunking is currently only optimized for PDF documents.")
        
    temp_file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # Process the file via Docling layout engine
        result = docling_converter.convert(temp_file_path)
        
        # Initialize the intelligent hybrid chunker
        chunker = HybridChunker(max_tokens=400)
        
        # Dynamically loop through layout structures and assemble context-aware chunks
        chunks = []
        for c in chunker.chunk(result.document):
            
            heading_title = "General Context"
            if c.heading and len(c.heading) > 0:
                heading_title = " > ".join(c.heading) # Creates path format like "Section 1 > Subsection A"
                
            chunks.append({
                "heading": heading_title,
                "text_content": c.text_content
            })
            
        return {
            "filename": file.filename,
            "total_chunks": len(chunks),
            "chunks": chunks
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)