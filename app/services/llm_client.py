import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # gemini / openai
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# ---------------- Gemini ----------------
def call_gemini(text):
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(text)
    return response.text


# ---------------- OpenAI ----------------
def call_openai(text):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message["content"]


# ---------- Universal LLM Handler ----------
def analyze_text(text):
    if PROVIDER == "openai":
        return call_openai(text)
    return call_gemini(text)
