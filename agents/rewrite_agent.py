# agents/rewrite_agent.py
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class RewriteAgent:
    def __init__(self, model_name="models/gemini-2.5-flash"):
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)

    def suggest_clause(self, clause_name):
        prompt = f"""
You are a legal assistant. Suggest a simple example text for the following missing/weak clause in a contract:
Clause: {clause_name}

Rules:
- Use plain English
- Short, practical example
- Include key legal points
- Max 100 words
"""
        response = self.model.generate_content(prompt)
        return response.text.strip()
