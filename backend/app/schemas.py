from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Document Models

class DocumentBase(BaseModel):
    filename: str
    content_type: str
    size_bytes: int

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    status: Optional[str] = None
    tags: Optional[List[str]] = None

class Document(DocumentBase):
    id: str
    status: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# Analysis Models

class SummaryRequest(BaseModel):
    document_id: str
    max_length: int = Field(500, ge=100, le=2000)

class SummaryResponse(BaseModel):
    document_id: str
    summary: str
    token_count: int
    confidence: float

class InsightRequest(BaseModel):
    document_id: str

class InsightResponse(BaseModel):
    document_id: str
    key_topics: List[str]
    entities: dict
    sentiment: str
    confidence: float

class QARequest(BaseModel):
    document_id: str
    question: str = Field(..., min_length=5, max_length=1000)

class QAResponse(BaseModel):
    document_id: str
    question: str
    answer: str
    confidence: float
    sources: List[str]

# Search Models

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    top_k: int = Field(5, ge=1, le=50)
    similarity_threshold: float = Field(0.5, ge=0, le=1)

class SearchResult(BaseModel):
    document_id: str
    filename: str
    snippet: str
    similarity_score: float
    page: Optional[int] = None

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_results: int
    search_time_ms: float

# Error Models

class ErrorResponse(BaseModel):
    error: str
    detail: str
    status_code: int
    timestamp: datetime
