# Placeholder for helpers.py
"""
Helper utilities for the Sustainable Smart City Assistant
"""
import os
import json
import logging
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """Helper class for data processing operations"""
    
    @staticmethod
    def validate_csv_file(file_path: str) -> bool:
        """Validate if CSV file exists and is readable"""
        try:
            if not os.path.exists(file_path):
                return False
            df = pd.read_csv(file_path)
            return len(df) > 0
        except Exception as e:
            logger.error(f"CSV validation error: {e}")
            return False
    
    @staticmethod
    def clean_kpi_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess KPI data"""
        try:
            # Remove duplicates
            df = df.drop_duplicates()
            
            # Handle missing values
            df = df.fillna(method='ffill').fillna(method='bfill')
            
            # Ensure numeric columns are properly typed
            numeric_columns = df.select_dtypes(include=['object']).columns
            for col in numeric_columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    pass
            
            return df
        except Exception as e:
            logger.error(f"Data cleaning error: {e}")
            return df
    
    @staticmethod
    def calculate_kpi_stats(df: pd.DataFrame, column: str) -> Dict[str, float]:
        """Calculate basic statistics for KPI column"""
        try:
            if column not in df.columns:
                return {}
            
            stats = {
                'mean': df[column].mean(),
                'median': df[column].median(),
                'std': df[column].std(),
                'min': df[column].min(),
                'max': df[column].max(),
                'latest': df[column].iloc[-1] if len(df) > 0 else 0
            }
            return stats
        except Exception as e:
            logger.error(f"Stats calculation error: {e}")
            return {}

class FileHandler:
    """Helper class for file operations"""
    
    @staticmethod
    def save_uploaded_file(uploaded_file, upload_dir: str = "temp_uploads") -> str:
        """Save uploaded file and return file path"""
        try:
            # Create upload directory if it doesn't exist
            Path(upload_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{uploaded_file.name}"
            file_path = os.path.join(upload_dir, filename)
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            
            return file_path
        except Exception as e:
            logger.error(f"File save error: {e}")
            return ""
    
    @staticmethod
    def read_text_file(file_path: str) -> str:
        """Read content from text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Text file read error: {e}")
            return ""
    
    @staticmethod
    def cleanup_temp_files(directory: str = "temp_uploads", max_age_hours: int = 24):
        """Clean up temporary files older than specified hours"""
        try:
            if not os.path.exists(directory):
                return
            
            current_time = datetime.now()
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if current_time - file_modified > timedelta(hours=max_age_hours):
                    os.remove(file_path)
                    logger.info(f"Cleaned up old file: {filename}")
        except Exception as e:
            logger.error(f"Cleanup error: {e}")

class APIHelper:
    """Helper class for API operations"""
    
    @staticmethod
    def make_api_request(endpoint: str, method: str = "GET", data: Dict = None, 
                        base_url: str = "http://localhost:8000") -> Dict:
        """Make API request to backend"""
        try:
            url = f"{base_url}{endpoint}"
            
            if method.upper() == "GET":
                response = requests.get(url, params=data)
            elif method.upper() == "POST":
                response = requests.post(url, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {e}")
            return {"error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {"error": str(e)}

class TextProcessor:
    """Helper class for text processing operations"""
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 500) -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
    
    @staticmethod
    def extract_keywords(text: str, top_n: int = 5) -> List[str]:
        """Extract top keywords from text (simple implementation)"""
        try:
            # Simple keyword extraction based on word frequency
            words = text.lower().split()
            
            # Filter out common stop words
            stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                         'of', 'with', 'by', 'is', 'are', 'was', 'were', 'a', 'an'}
            
            filtered_words = [word.strip('.,!?;:"()[]') for word in words 
                            if word.lower() not in stop_words and len(word) > 2]
            
            # Count word frequency
            word_freq = {}
            for word in filtered_words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Return top N keywords
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [word[0] for word in sorted_words[:top_n]]
        except Exception as e:
            logger.error(f"Keyword extraction error: {e}")
            return []
    
    @staticmethod
    def format_response_text(text: str) -> str:
        """Format AI response text for better display"""
        try:
            # Remove extra whitespace
            text = ' '.join(text.split())
            
            # Ensure proper sentence endings
            if text and not text.endswith(('.', '!', '?')):
                text += '.'
            
            return text
        except Exception as e:
            logger.error(f"Text formatting error: {e}")
            return text

class ConfigHelper:
    """Helper class for configuration management"""
    
    @staticmethod
    def get_city_kpi_config() -> Dict[str, List[str]]:
        """Get KPI configuration for different cities"""
        return {
            "New York": ["water_usage", "air_quality", "energy_consumption", "waste_management"],
            "London": ["water_usage", "air_quality", "energy_consumption", "transportation"],
            "Tokyo": ["water_usage", "air_quality", "energy_consumption", "population_density"],
            "Mumbai": ["water_usage", "air_quality", "energy_consumption", "waste_management"],
            "Default": ["water_usage", "air_quality", "energy_consumption"]
        }
    
    @staticmethod
    def get_feedback_categories() -> List[str]:
        """Get available feedback categories"""
        return [
            "Water Management",
            "Air Quality",
            "Energy Efficiency",
            "Waste Management",
            "Transportation",
            "Green Spaces",
            "Public Safety",
            "Digital Services",
            "Other"
        ]
    
    @staticmethod
    def get_eco_tip_categories() -> List[str]:
        """Get available eco tip categories"""
        return [
            "Energy Conservation",
            "Water Saving",
            "Waste Reduction",
            "Sustainable Transport",
            "Green Living",
            "Renewable Energy",
            "Air Quality",
            "Climate Action"
        ]

class ValidationHelper:
    """Helper class for data validation"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Simple email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_feedback_data(data: Dict) -> Dict[str, str]:
        """Validate feedback form data"""
        errors = {}
        
        if not data.get('name', '').strip():
            errors['name'] = "Name is required"
        
        if not data.get('category', '').strip():
            errors['category'] = "Category is required"
        
        if not data.get('message', '').strip():
            errors['message'] = "Message is required"
        elif len(data['message']) < 10:
            errors['message'] = "Message must be at least 10 characters long"
        
        email = data.get('email', '').strip()
        if email and not ValidationHelper.validate_email(email):
            errors['email'] = "Invalid email format"
        
        return errors
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Basic input sanitization"""
        if not isinstance(text, str):
            return ""
        
        # Remove potentially harmful characters
        import re
        sanitized = re.sub(r'[<>"\']', '', text)
        return sanitized.strip()

def format_number(value: float, unit: str = "") -> str:
    """Format number for display with appropriate units"""
    try:
        if value >= 1000000:
            return f"{value/1000000:.1f}M {unit}"
        elif value >= 1000:
            return f"{value/1000:.1f}K {unit}"
        else:
            return f"{value:.1f} {unit}"
    except:
        return f"{value} {unit}"

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()

def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Safely divide two numbers"""
    try:
        return a / b if b != 0 else default
    except:
        return default