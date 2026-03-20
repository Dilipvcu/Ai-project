from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services (lazy loading)
_llm_service = None
_embedding_service = None
_db_service = None

async def initialize_services():
    """Initialize all services on startup"""
    global _llm_service, _embedding_service, _db_service
    from app.services.llm_service import LLMService
    from app.services.embedding_service import EmbeddingService
    from app.services.database_service import DatabaseService
    
    _llm_service = LLMService(api_key=os.getenv("OPENAI_API_KEY"))
    _embedding_service = EmbeddingService()
    _db_service = DatabaseService()
    logger.info("✅ All services initialized")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    await initialize_services()
    logger.info("🚀 Application started")
    yield
    # Shutdown
    logger.info("🛑 Application shutting down")

# Initialize FastAPI app
app = FastAPI(
    title="AI Document Analysis Engine",
    description="Smart document analysis with AI-powered insights",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", 
    "http://localhost:3000,http://localhost:3001,http://localhost:8080,https://ai-project-production-fdb3.up.railway.app"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "llm": "ready" if _llm_service else "initializing",
            "embeddings": "ready" if _embedding_service else "initializing",
            "database": "ready" if _db_service else "initializing"
        }
    }

# Import routers
from app.api import documents, analysis, search

# Include routers
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(search.router, prefix="/api/search", tags=["search"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🤖 AI Document Analysis Engine",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
