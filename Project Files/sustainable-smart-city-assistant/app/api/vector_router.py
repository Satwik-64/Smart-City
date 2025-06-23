# Placeholder for vector_router.py
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.document_embedder import DocumentEmbedder
from app.services.document_retriever import DocumentRetriever
import tempfile
import os

router = APIRouter()

class DocumentUploadResponse(BaseModel):
    filename: str
    document_id: str
    chunks_created: int
    status: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    total_found: int
    status: str

# Initialize services
document_embedder = DocumentEmbedder()
document_retriever = DocumentRetriever()

@router.post("/upload-document", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and embed a policy document"""
    try:
        # Validate file type
        if not file.filename.endswith(('.txt', '.pdf', '.docx')):
            raise HTTPException(
                status_code=400, 
                detail="Only .txt, .pdf, and .docx files are supported"
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            contents = await file.read()
            tmp_file.write(contents)
            tmp_file_path = tmp_file.name
        
        try:
            # Process and embed the document
            result = document_embedder.embed_document(tmp_file_path, file.filename)
            
            return DocumentUploadResponse(
                filename=file.filename,
                document_id=result["document_id"],
                chunks_created=result["chunks_created"],
                status="success"
            )
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """Search for relevant policy documents"""
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        results = document_retriever.search_documents(request.query, top_k=request.top_k)
        
        return SearchResponse(
            query=request.query,
            results=results,
            total_found=len(results),
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")

@router.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    try:
        documents = document_retriever.list_all_documents()
        return {"documents": documents, "count": len(documents)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@router.delete("/documents/{document_id}")
async def delete_document(document_id: str):
    """Delete a document and its embeddings"""
    try:
        success = document_retriever.delete_document(document_id)
        if success:
            return {"message": f"Document {document_id} deleted successfully", "status": "success"}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")
