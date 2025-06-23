# Placeholder for chat_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.granite_llm import granite_llm

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    status: str

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """Handle chat queries using Granite LLM"""
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        response = granite_llm.ask_granite(request.message)
        
        return ChatResponse(
            response=response,
            status="success"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")
