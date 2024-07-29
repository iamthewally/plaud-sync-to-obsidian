import requests
import json
import logging
from config import OLLAMA_ENDPOINT, LLM_MODEL

def generate_summary_and_hashtags(transcript):
    prompt = f"""Based on the following transcript, provide a short summary (2-3 sentences) and generate 3-5 relevant hashtags. Format the output as JSON with 'summary' and 'hashtags' keys.

Transcript:
{transcript}

Output format:
{{
  "summary": "Your summary here",
  "hashtags": ["#tag1", "#tag2", "#tag3"]
}}
"""
    
    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_ENDPOINT, json=payload)
        
        if response.status_code == 200:
            try:
                result = json.loads(response.json()['response'])
                return result['summary'], result['hashtags']
            except json.JSONDecodeError:
                logging.error("Failed to parse LLM response as JSON")
                return "", []
        else:
            logging.error(f"LLM processing failed with status code {response.status_code}")
            return "", []
    except Exception as e:
        logging.error(f"Error during LLM processing: {e}")
        return "", []