import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealth:
    def test_health_check(self):
        """Test health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

class TestDocuments:
    def test_upload_document(self):
        """Test document upload"""
        with open("test_file.txt", "wb") as f:
            f.write(b"Test content")
        
        with open("test_file.txt", "rb") as f:
            files = {"file": f}
            response = client.post("/api/documents/upload", files=files)
        
        assert response.status_code == 200
        assert "document_id" in response.json()
    
    def test_list_documents(self):
        """Test listing documents"""
        response = client.get("/api/documents")
        assert response.status_code == 200
        assert "documents" in response.json()
    
    def test_get_nonexistent_document(self):
        """Test getting non-existent document"""
        response = client.get("/api/documents/nonexistent")
        assert response.status_code == 404

class TestAnalysis:
    def test_summarize_document(self):
        """Test document summarization"""
        response = client.post(
            "/api/analysis/summarize",
            json={"document_id": "test-id", "max_length": 500}
        )
        # Should handle gracefully
        assert response.status_code in [200, 400, 404]
    
    def test_extract_insights(self):
        """Test insight extraction"""
        response = client.post(
            "/api/analysis/extract-insights",
            json={"document_id": "test-id"}
        )
        assert response.status_code in [200, 400, 404]

class TestSearch:
    def test_semantic_search(self):
        """Test semantic search"""
        response = client.post(
            "/api/search/semantic",
            json={"query": "test query", "top_k": 5}
        )
        assert response.status_code == 200
        assert "results" in response.json()
    
    def test_search_suggestions(self):
        """Test search suggestions"""
        response = client.get("/api/search/suggestions?prefix=test")
        assert response.status_code == 200
        assert "suggestions" in response.json()
