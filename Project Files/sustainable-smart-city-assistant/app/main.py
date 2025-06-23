# Placeholder for main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api import (
    chat_router, 
    feedback_router, 
    eco_tips_router,
    kpi_upload_router,
    vector_router,
    policy_router,
    dashboard_router
)
from dotenv import load_dotenv
load_dotenv()  # Load environment variables

app = FastAPI(
    title="Sustainable Smart City Assistant API",
    description="AI-powered platform for urban sustainability and governance",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router.router, prefix="/api/chat", tags=["chat"])
app.include_router(feedback_router.router, prefix="/api/feedback", tags=["feedback"])
app.include_router(eco_tips_router.router, prefix="/api/eco-tips", tags=["eco-tips"])
app.include_router(kpi_upload_router.router, prefix="/api/kpi", tags=["kpi"])
app.include_router(vector_router.router, prefix="/api/vector", tags=["vector"])
app.include_router(policy_router.router, prefix="/api/policy", tags=["policy"])
app.include_router(dashboard_router.router, prefix="/api/dashboard", tags=["dashboard"])

@app.get("/")
async def root():
    return {"message": "Sustainable Smart City Assistant API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is operational"}
