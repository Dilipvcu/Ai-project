from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import Optional, List
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory storage for demo (replace with real DB)
documents_store = {}

class DocumentUploadResponse:
    def __init__(self, document_id: str, filename: str, status: str, size_bytes: int):
        self.document_id = document_id
        self.filename = filename
        self.status = status
        self.size_bytes = size_bytes
        self.uploaded_at = datetime.utcnow().isoformat()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Upload a document for analysis
    
    Supported formats: PDF, DOCX, TXT, Images (PNG, JPG)
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="Filename required")
        
        # Check file size (max 50MB)
        contents = await file.read()
        file_size = len(contents)
        
        if file_size > 50 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large (max 50MB)")
        
        # Generate document ID
        document_id = str(uuid.uuid4())
        
        # Store metadata
        documents_store[document_id] = {
            "id": document_id,
            "filename": file.filename,
            "size_bytes": file_size,
            "status": "processing",
            "uploaded_at": datetime.utcnow().isoformat(),
            "content_type": file.content_type
        }
        
        # Schedule background processing
        if background_tasks:
            background_tasks.add_task(process_document, document_id, contents)
        
        logger.info(f"📄 Document uploaded: {document_id} ({file.filename})")
        
        return {
            "document_id": document_id,
            "filename": file.filename,
            "status": "processing",
            "size_bytes": file_size,
            "message": "Document queued for analysis"
        }
    
    except Exception as e:
        logger.error(f"❌ Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}")
async def get_document(document_id: str):
    """Retrieve document details and analysis results"""
    
    if document_id not in documents_store:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc = documents_store[document_id]
    return {
        "id": doc["id"],
        "filename": doc["filename"],
        "status": doc["status"],
        "size_bytes": doc["size_bytes"],
        "uploaded_at": doc["uploaded_at"],
        "content_type": doc["content_type"]
    }

@router.get("")
async def list_documents(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None
):
    """List all uploaded documents with pagination"""
    
    documents = list(documents_store.values())
    
    if status:
        documents = [d for d in documents if d["status"] == status]
    
    # Pagination
    total = len(documents)
    documents = documents[skip:skip + limit]
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "documents": documents
    }

@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and its associated data"""
    
    if document_id not in documents_store:
        raise HTTPException(status_code=404, detail="Document not found")
    
    filename = documents_store[document_id]["filename"]
    del documents_store[document_id]
    
    logger.info(f"🗑️ Document deleted: {document_id} ({filename})")
    
    return {
        "message": "Document deleted successfully",
        "document_id": document_id
    }

async def process_document(document_id: str, content: bytes):
    """Background task to process uploaded document"""
    try:
        logger.info(f"⚙️ Processing document: {document_id}")
        
        # Simulate processing
        from app.services.document_processor import DocumentProcessor
        processor = DocumentProcessor()
        
        # Extract text
        text = await processor.extract_text(content)
        
        # Generate embeddings
        from app.services.embedding_service import EmbeddingService
        embedder = EmbeddingService()
        embeddings = await embedder.embed(text)
        
        # Update status
        documents_store[document_id]["status"] = "completed"
        documents_store[document_id]["text_length"] = len(text)
        documents_store[document_id]["embedding_count"] = len(embeddings)
        
        logger.info(f"✅ Document processed: {document_id}")
        
    except Exception as e:
        logger.error(f"❌ Processing error for {document_id}: {str(e)}")
        documents_store[document_id]["status"] = "failed"
        documents_store[document_id]["error"] = str(e)
