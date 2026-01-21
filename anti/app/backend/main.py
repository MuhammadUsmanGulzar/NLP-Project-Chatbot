from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
import uvicorn
from app.backend.core.ingestion import IngestionService
from app.backend.core.retrieval import RetrievalService
from app.backend.core.generation import GenerationService

app = FastAPI(title="Local RAG Chatbot")

# Initialize Services
# NOTE: Ensure you have 'llama3' pulled in Ollama. 
# You can change model_name to 'mistral' or others if needed.
ingestion_service = IngestionService()
retrieval_service = RetrievalService()
generation_service = GenerationService(model_name="gemma:2b")

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
    context: list[str]

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Load and process
        text = ingestion_service.load_file(file_location)
        chunks = ingestion_service.chunk_text(text)
        
        # Add to vector store
        retrieval_service.add_documents(chunks)
        
        return {"message": f"Successfully ingested {file.filename}", "chunks_added": len(chunks)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Retrieve context
        context_chunks = retrieval_service.search(request.query, k=3)
        
        # Generate answer
        answer = generation_service.generate_response(request.query, context_chunks)
        
        return ChatResponse(response=answer, context=context_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.backend.main:app", host="0.0.0.0", port=8000, reload=True)
