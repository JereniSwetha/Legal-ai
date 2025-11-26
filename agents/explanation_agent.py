import google.generativeai as genai

class ExplanationAgent:
    def __init__(self, model_name="models/gemini-2.5-flash"):
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)

    def explain_clause(self, clause, text):
     prompt = f"""Explain this legal clause in SIMPLE terms (like explaining to a 15-year-old):
    
Clause: {clause}

From text: {text}

Rules:
- Use short, simple sentences
- Avoid legal jargon (or explain it simply)
- Use everyday examples
- Say what it means in practice
- Say why it matters

Keep it under 150 words."""

     response = self.model.generate_content(prompt)
     return response.text