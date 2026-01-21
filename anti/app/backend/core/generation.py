import requests
import json
from typing import List

class GenerationService:
    def __init__(self, model_name: str = "llama3", ollama_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.api_endpoint = f"{self.ollama_url}/api/generate"

    def generate_response(self, query: str, context_chunks: List[str]) -> str:
        """Generates a response using Ollama with RAG context."""
        
        context_text = "\n\n".join(context_chunks)
        
        prompt = f"""
        Instructions:
        You are a helpful assistant. You must answer the user's question explicitly based on the provided Context below. 
        If the Context contains the answer, summarizing it or extracting the relevant part.
        Do not say you don't have information if it is clearly in the Context.

        Context:
        {context_text}
        
        User Question: {query}
        
        Answer:
        """
        
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            print(f"Sending request to Ollama ({self.model_name})...")
            # Added 300s timeout (5 mins) for slower machines
            response = requests.post(self.api_endpoint, json=payload, timeout=300) 
            response.raise_for_status()
            result = response.json()
            return result.get("response", "Error: No response field in output.")
        except requests.exceptions.Timeout:
            return "Error: Request to Ollama timed out. The model might be too large for your PC or is taking too long to load."
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {e}"

if __name__ == "__main__":
    # Test
    gen = GenerationService()
    print("Generation Service Initialized")
