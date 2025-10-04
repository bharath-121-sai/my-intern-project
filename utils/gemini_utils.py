import requests
import json

# ----------------- Configuration -----------------
API_KEY = "AIzaSyCwDdc4ikmizcWYopwToN6qVFDzP9Gigms"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key="


def generate_summary(text):
    """Generate summary for a given PDF text."""
    payload = {
        "contents": [{"parts": [{"text": f"Summarize this research paper in detail:\n\n{text}"}]}]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{API_URL}{API_KEY}", headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]

def answer_question(text, question):
    """Answer question based on given PDF text."""
    prompt = f"You are a research assistant. Based on this paper:\n\n{text}\n\nAnswer this question: {question}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{API_URL}{API_KEY}", headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]
