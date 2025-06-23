# Placeholder for config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # IBM Watsonx Settings
    watsonx_api_key: str
    watsonx_project_id: str
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    watsonx_model_id: str = "ibm/granite-13b-instruct-v2"
    
    # Pinecone Settings
    pinecone_api_key: str
    pinecone_env: str
    index_name: str = "smartcity-policies"
    
    # Application Settings
    debug: bool = True
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    frontend_port: int = 8501
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
