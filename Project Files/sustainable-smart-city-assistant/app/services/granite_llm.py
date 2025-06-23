import requests
import json
from app.core.config import settings
from typing import Optional, Dict, Any

class GraniteLLM:
    def __init__(self):
        self.api_key = settings.watsonx_api_key
        self.project_id = settings.watsonx_project_id
        self.url = settings.watsonx_url
        self.model_id = settings.watsonx_model_id
        self.token = self._get_iam_token()

    def _get_iam_token(self) -> Optional[str]:
        """Obtain IAM access token using API key"""
        try:
            response = requests.post(
                "https://iam.cloud.ibm.com/identity/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                    "apikey": self.api_key
                },
                timeout=15
            )
            response.raise_for_status()
            return response.json().get("access_token")
        except Exception as e:
            print(f"[Granite LLM] IAM Token Error: {e}")
            return None

    def _make_request(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """Make request to IBM Watsonx Granite LLM"""
        if not self.token:
            print("[Granite LLM] No valid IAM token available.")
            return None

        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.token}"
    }

        payload = {
        "model_id": self.model_id,
        "input": prompt,
        "project_id": self.project_id,
        "parameters": {
            "decoding_method": "greedy",  # or "sample"
            "max_new_tokens": max_tokens,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 1.0,
            "repetition_penalty": 1.1
        }
    }

        try:
            response = requests.post(
    f"{self.url}/ml/v1-beta/generation/text?version=2024-05-01",
    headers=headers,
    json=payload,
    timeout=30
)

            response.raise_for_status()
            result = response.json()
            return result.get("results", [{}])[0].get("generated_text", "")
        except requests.exceptions.HTTPError as e:
            print(f"[Granite LLM] HTTPError: {e} - Response: {response.text}")
            return None
        except Exception as e:
            print(f"[Granite LLM] General Error: {e}")
            return None

    def ask_granite(self, prompt: str) -> str:
        system_prompt = """You are a helpful assistant for a smart city platform. 
        Provide informative, concise answers about urban sustainability, governance, and smart city technologies."""

        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
        response = self._make_request(full_prompt)
        return response or "I'm sorry, I couldn't process your request at the moment."

    def generate_summary(self, text: str) -> str:
        prompt = f"""Summarize the following policy document in a clear, citizen-friendly format:\n\n{text}\n\nSummary:"""
        response = self._make_request(prompt, max_tokens=300)
        return response or "Unable to generate summary."

    def generate_eco_tip(self, topic: str) -> str:
        prompt = f"""Generate 3 practical, actionable eco-friendly tips related to "{topic}" for city residents:\n\nTips:"""
        response = self._make_request(prompt, max_tokens=200)
        return response or f"Here are some general tips for {topic}: reduce consumption, reuse materials, and recycle properly."

    def generate_city_report(self, city_name: str, kpi_data: Dict[str, Any]) -> str:
        prompt = f"""Generate a comprehensive sustainability report for {city_name} based on the following KPI data:\n\n{json.dumps(kpi_data, indent=2)}\n\nReport:"""
        response = self._make_request(prompt, max_tokens=800)
        return response or "Unable to generate report."

# Create singleton instance
granite_llm = GraniteLLM()
