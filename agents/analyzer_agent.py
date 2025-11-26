import google.generativeai as genai
from agents.clauses import find_clauses, CLAUSE_PATTERNS
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class AnalyzerAgent:
    def __init__(self, model_name="models/gemini-2.5-flash"):
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        self.known_clauses = list(CLAUSE_PATTERNS.keys())

    def analyze(self, text, llm_fallback_for=[]):
        # Step 1: Regex-based detection
        regex_found = find_clauses(text)
        
        # Step 2: LLM-based analysis
        prompt = f"""Analyze this legal document. 
        
Known clauses: {', '.join(self.known_clauses)}

Document:
{text}

Return JSON:
{{
    "missing_clauses": ["list of missing clauses"],
    "weak_clauses": ["list of weak clauses"],
    "risky_clauses": ["list of risky clauses"],
    "llm_checks": {{"clause": {{"confidence": 90, "description": "details"}}}}
}}"""

        response = self.model.generate_content(prompt)
        
        # Clean markdown
        clean_text = response.text.strip()
        clean_text = re.sub(r'^```(json)?\n', '', clean_text)
        clean_text = re.sub(r'\n```$', '', clean_text)
        
        try:
            result = json.loads(clean_text)
        except json.JSONDecodeError:
            result = {
                "missing_clauses": [],
                "weak_clauses": [],
                "risky_clauses": [],
                "raw_analysis": response.text
            }
        
        return json.dumps(result)