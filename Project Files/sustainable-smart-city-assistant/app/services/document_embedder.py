# Placeholder for document_embedder.py
from sentence_transformers import SentenceTransformer
from app.services.pinecone_client import pinecone_client
import hashlib
import uuid
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DocumentEmbedder:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunk_size = 500  # Characters per chunk
        self.overlap = 50      # Character overlap between chunks
    
    def embed_document(self, file_path: str, filename: str) -> Dict[str, Any]:
        """Embed a document and store in Pinecone"""
        try:
            # Read document content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Create document ID
            document_id = self._generate_document_id(filename)
            
            # Split into chunks
            chunks = self._split_into_chunks(content)
            
            # Generate embeddings
            embeddings = self.model.encode(chunks)
            
            # Prepare vectors for Pinecone
            vectors = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                vector_id = f"{document_id}_chunk_{i}"
                vectors.append({
                    "id": vector_id,
                    "values": embedding.tolist(),
                    "metadata": {
                        "document_id": document_id,
                        "filename": filename,
                        "chunk_index": i,
                        "content": chunk,
                        "content_length": len(chunk)
                    }
                })
            
            # Upload to Pinecone
            success = pinecone_client.upsert_vectors(vectors)
            
            if success:
                logger.info(f"Successfully embedded document: {filename}")
                return {
                    "document_id": document_id,
                    "chunks_created": len(chunks),
                    "status": "success"
                }
            else:
                raise Exception("Failed to upload vectors to Pinecone")
                
        except Exception as e:
            logger.error(f"Error embedding document {filename}: {e}")
            raise
    
    def _generate_document_id(self, filename: str) -> str:
        """Generate unique document ID"""
        # Use filename and current timestamp to create unique ID
        unique_string = f"{filename}_{uuid.uuid4()}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]
    
    def _split_into_chunks(self, content: str) -> List[str]:
        """Split document content into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(content):
            # Calculate end position
            end = min(start + self.chunk_size, len(content))
            
            # Find the last sentence boundary within the chunk
            if end < len(content):
                # Look for sentence endings
                for punct in ['. ', '! ', '? ', '\n\n']:
                    last_punct = content.rfind(punct, start, end)
                    if last_punct != -1:
                        end = last_punct + len(punct)
                        break
            
            chunk = content[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = max(start + self.chunk_size - self.overlap, end)
        
        return chunks
