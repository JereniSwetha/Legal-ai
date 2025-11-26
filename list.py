# list.py
import google.generativeai as genai
from utils.gemini_client import genai  # assumes you configured API key there

models = genai.list_models()

for m in models:
    # print basic info safely
    print(f"Name: {m.name}")
    print(f"Description: {getattr(m, 'description', 'No description')}")
    print(f"Availability: {getattr(m, 'availability', 'Unknown')}")
    print(f"Parameters: {getattr(m, 'parameters', {})}")
    print("-" * 40)
