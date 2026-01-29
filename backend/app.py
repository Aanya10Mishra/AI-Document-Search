from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import PyPDF2
from docx import Document
import io
import os
from typing import List
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Document Search API")

# CORS middleware (allows frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models and databases
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "")
hf_client = InferenceClient(token=HF_TOKEN) if HF_TOKEN else None

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

chroma_client = chromadb.Client(Settings(
    persist_directory="./chroma_db",
    anonymized_telemetry=False
))

try:
    collection = chroma_client.get_collection("documents")
except:
    collection = chroma_client.create_collection("documents")

# Pydantic models
class QueryRequest(BaseModel):
    question: str
    n_results: int = 3

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

# Helper functions
def extract_text_from_pdf(file_content):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_content):
    doc = Document(io.BytesIO(file_content))
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

def extract_text_from_txt(file_content):
    return file_content.decode('utf-8')

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def add_document_to_db(text, filename):
    chunks = chunk_text(text)
    if not chunks:
        return 0
    
    embeddings = embedding_model.encode(chunks).tolist()
    ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename, "chunk_id": i} for i in range(len(chunks))]
    
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    
    return len(chunks)

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "AI Document Search API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Read file content
        content = await file.read()
        
        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(content)
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(content)
        elif file.filename.endswith('.txt'):
            text = extract_text_from_txt(content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Add to database
        chunks_added = add_document_to_db(text, file.filename)
        
        return {
            "message": "Document processed successfully",
            "filename": file.filename,
            "chunks_added": chunks_added
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Search documents and generate answer"""
    try:
        # Generate query embedding
        query_embedding = embedding_model.encode([request.question]).tolist()
        
        # Search vector database
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=request.n_results
        )
        
        if not results['documents'] or len(results['documents'][0]) == 0:
            return QueryResponse(
                answer="No relevant documents found. Please upload documents first.",
                sources=[]
            )
        
        # Prepare context
        context = "\n\n".join(results['documents'][0])
        
        # Generate answer
        prompt = f"""You are a helpful assistant. Answer the question based on the provided context.

Context:
{context}

Question: {request.question}

Answer:"""
        
        # Use Hugging Face API if token available, else use local generation
        if hf_client:
            try:
                answer = hf_client.text_generation(
                    prompt,
                    model="mistralai/Mistral-7B-Instruct-v0.2",
                    max_new_tokens=500,
                    temperature=0.7
                )
            except:
                answer = "Based on the documents: " + context[:300] + "..."
        else:
            # Fallback: simple extraction
            answer = f"Based on the context: {context[:500]}..."
        
        # Prepare sources
        sources = []
        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
            sources.append({
                "source": metadata['source'],
                "chunk_id": metadata['chunk_id'],
                "text": doc[:200] + "..." if len(doc) > 200 else doc
            })
        
        return QueryResponse(answer=answer, sources=sources)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_stats():
    """Get database statistics"""
    try:
        count = collection.count()
        return {"total_chunks": count}
    except:
        return {"total_chunks": 0}

@app.delete("/clear")
def clear_database():
    """Clear all documents from database"""
    global collection
    try:
        chroma_client.delete_collection("documents")
        collection = chroma_client.create_collection("documents")
        return {"message": "Database cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


