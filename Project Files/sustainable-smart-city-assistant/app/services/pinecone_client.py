# app/services/pinecone_client.py
import os
import logging
from typing import Optional
import pinecone

logger = logging.getLogger(__name__)

class PineconeClient:
    def __init__(self):
        self.client = None
        self.index = None
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "sustainable-city-docs")
        self._initialized = False
        self._initialization_attempted = False
    
    def _initialize_client(self):
        """Initialize Pinecone client with error handling"""
        if self._initialization_attempted:
            return self._initialized
            
        self._initialization_attempted = True
        
        try:
            api_key = os.getenv("PINECONE_API_KEY")
            environment = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-gcp")
            
            if not api_key:
                logger.warning("PINECONE_API_KEY not found. Running in offline mode.")
                return False
            
            # Initialize Pinecone
            pinecone.init(api_key=api_key, environment=environment)
            
            # Check if index exists
            existing_indexes = pinecone.list_indexes()
            if self.index_name not in existing_indexes:
                logger.warning(f"Index '{self.index_name}' not found. Creating new index...")
                pinecone.create_index(
                    name=self.index_name,
                    dimension=768,  # Adjust based on your embedding model
                    metric="cosine"
                )
            
            # Connect to index
            self.index = pinecone.Index(self.index_name)
            self._initialized = True
            logger.info("Pinecone client initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Pinecone: {e}")
            logger.info("Continuing in offline mode...")
            return False
    
    def is_available(self) -> bool:
        """Check if Pinecone is available"""
        if not self._initialization_attempted:
            self._initialize_client()
        return self._initialized
    
    def upsert_vectors(self, vectors, namespace="default"):
        """Upsert vectors to Pinecone"""
        if not self.is_available():
            logger.warning("Pinecone not available. Vectors not stored.")
            return {"upserted_count": 0, "status": "offline"}
        
        try:
            response = self.index.upsert(vectors=vectors, namespace=namespace)
            return response
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            return {"error": str(e)}
    
    def query_vectors(self, vector, top_k=5, namespace="default", include_metadata=True):
        """Query vectors from Pinecone"""
        if not self.is_available():
            logger.warning("Pinecone not available. Returning empty results.")
            return {"matches": [], "status": "offline"}
        
        try:
            response = self.index.query(
                vector=vector,
                top_k=top_k,
                namespace=namespace,
                include_metadata=include_metadata
            )
            return response
        except Exception as e:
            logger.error(f"Error querying vectors: {e}")
            return {"matches": [], "error": str(e)}
    
    def delete_vectors(self, ids, namespace="default"):
        """Delete vectors from Pinecone"""
        if not self.is_available():
            logger.warning("Pinecone not available. Cannot delete vectors.")
            return {"status": "offline"}
        
        try:
            response = self.index.delete(ids=ids, namespace=namespace)
            return response
        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            return {"error": str(e)}

# Create a singleton instance but don't initialize immediately
pinecone_client = PineconeClient()