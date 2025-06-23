# Placeholder for document_retriever.py
from sentence_transformers import SentenceTransformer
from app.services.pinecone_client import pinecone_client
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DocumentRetriever:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def search_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant document chunks"""
        try:
            # Generate query embedding
            query_embedding = self.model.encode([query])[0]

            # Search in Pinecone
            results = pinecone_client.query_vectors(
                vector=query_embedding.tolist(),
                top_k=top_k
            )

            # Format results
            formatted_results = []
            for match in results:
                result = {
                    "id": match.get("id", ""),
                    "score": match.get("score", 0.0),
                    "metadata": match.get("metadata", {}),
                    "content": match.get("metadata", {}).get("content", ""),
                    "filename": match.get("metadata", {}).get("filename", ""),
                    "document_id": match.get("metadata", {}).get("document_id", "")
                }
                formatted_results.append(result)

            logger.info(f"Found {len(formatted_results)} results for query: {query}")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching documents: {e}")
            return []

    def get_document_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve all chunks for a specific document"""
        try:
            # This would require a different approach with Pinecone
            # For now, we'll search with a broad query to find document chunks
            # In production, you might want to store document metadata separately
            results = self.search_documents(f"document_id:{document_id}", top_k=100)

            # Filter results by document ID
            document_chunks = [
                result for result in results
                if result.get("document_id") == document_id
            ]

            if document_chunks:
                # Combine chunks into full document
                full_content = " ".join([
                    chunk["content"] for chunk in
                    sorted(document_chunks, key=lambda x: x.get("metadata", {}).get("chunk_index", 0))
                ])

                return {
                    "document_id": document_id,
                    "filename": document_chunks[0].get("filename", ""),
                    "content": full_content,
                    "chunks": len(document_chunks)
                }

            return None

        except Exception as e:
            logger.error(f"Error retrieving document {document_id}: {e}")
            return None

    def list_all_documents(self) -> List[Dict[str, Any]]:
        """List all uploaded documents"""
        try:
            # This is a simplified approach - in production you'd want
            # a separate metadata store for document management
            results = self.search_documents("document", top_k=1000)

            # Group by document_id
            documents = {}
            for result in results:
                doc_id = result.get("document_id")
                if doc_id and doc_id not in documents:
                    documents[doc_id] = {
                        "document_id": doc_id,
                        "filename": result.get("filename", ""),
                        "chunk_count": 1
                    }
                elif doc_id:
                    documents[doc_id]["chunk_count"] += 1

            return list(documents.values())

        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return []

    def delete_document(self, document_id: str) -> bool:
        """Delete a document and all its chunks"""
        try:
            # Find all chunks for this document
            results = self.search_documents(f"document_id:{document_id}", top_k=1000)

            # Extract chunk IDs that belong to this document
            chunk_ids = [
                result["id"] for result in results
                if result.get("document_id") == document_id
            ]

            if chunk_ids:
                # Delete vectors from Pinecone
                success = pinecone_client.delete_vectors(chunk_ids)
                if success:
                    logger.info(f"Successfully deleted document {document_id} with {len(chunk_ids)} chunks")
                    return True
                else:
                    logger.error(f"Failed to delete vectors for document {document_id}")
                    return False
            else:
                logger.warning(f"No chunks found for document {document_id}")
                return False

        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            return False