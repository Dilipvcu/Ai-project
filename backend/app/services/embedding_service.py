import logging
from typing import List, Dict, Optional
import numpy as np

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Service for generating and managing embeddings
    
    Converts text to vector embeddings for semantic search
    Supports OpenAI Embeddings API and Sentence Transformers
    """
    
    def __init__(self, model: str = "text-embedding-3-small"):
        """
        Initialize embedding service
        
        Args:
            model: Embedding model to use
                - text-embedding-3-small (OpenAI)
                - text-embedding-3-large (OpenAI)
                - all-MiniLM-L6-v2 (Sentence Transformers)
        """
        self.model = model
        self.embedding_dim = 1536 if "3-small" in model else 1024
        logger.info(f"🔢 Embedding Service initialized with model: {model}")
    
    async def embed(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
        
        Returns:
            Vector embedding (list of floats)
        """
        try:
            if not text or len(text.strip()) == 0:
                raise ValueError("Text cannot be empty")
            
            logger.info(f"📝 Generating embedding for text (length: {len(text)})")
            
            # This would call OpenAI API or local model
            # For demo, return random vector
            embedding = np.random.randn(self.embedding_dim).tolist()
            return embedding
        
        except Exception as e:
            logger.error(f"❌ Embedding generation failed: {str(e)}")
            raise
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts (more efficient)
        
        Args:
            texts: List of texts to embed
        
        Returns:
            List of embeddings
        """
        try:
            logger.info(f"📚 Generating {len(texts)} embeddings (batch)")
            
            embeddings = []
            for text in texts:
                emb = await self.embed(text)
                embeddings.append(emb)
            
            return embeddings
        
        except Exception as e:
            logger.error(f"❌ Batch embedding failed: {str(e)}")
            raise
    
    async def search(
        self,
        query: str,
        document_embeddings: Dict[str, List[float]],
        top_k: int = 5,
        threshold: float = 0.5
    ) -> List[Dict]:
        """
        Search similar documents using vector similarity
        
        Args:
            query: Search query
            document_embeddings: Dict of {doc_id: embedding}
            top_k: Number of results to return
            threshold: Minimum similarity threshold
        
        Returns:
            Ranked list of similar documents
        """
        try:
            logger.info(f"🔍 Semantic search for: '{query}' (top_k={top_k})")
            
            # Get query embedding
            query_embedding = await self.embed(query)
            
            # Compute similarities
            similarities = {}
            for doc_id, doc_embedding in document_embeddings.items():
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                if similarity >= threshold:
                    similarities[doc_id] = similarity
            
            # Sort and return top-k
            ranked = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]
            
            return [
                {"document_id": doc_id, "similarity_score": float(score)}
                for doc_id, score in ranked
            ]
        
        except Exception as e:
            logger.error(f"❌ Search failed: {str(e)}")
            raise
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Compute cosine similarity between two vectors"""
        try:
            v1 = np.array(vec1)
            v2 = np.array(vec2)
            
            dot_product = np.dot(v1, v2)
            magnitude1 = np.linalg.norm(v1)
            magnitude2 = np.linalg.norm(v2)
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            return float(dot_product / (magnitude1 * magnitude2))
        
        except Exception as e:
            logger.error(f"❌ Similarity computation failed: {str(e)}")
            return 0.0
